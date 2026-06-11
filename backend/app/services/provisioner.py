"""SSH Auto-Provisioner — the heart of AI One.

SSH into a target server, detect OS, install Docker if needed,
deploy the agent container, and register it in the central registry.
"""

import asyncio
import os
import socket
import uuid
from typing import Any

import paramiko


async def provision_agent(
    host: str,
    port: int,
    username: str,
    password: str,
    agent_id: uuid.UUID,
    agent_name: str,
    role: str = "worker",
    hub_url: str = "http://backend:8000",
) -> dict[str, Any]:
    """Provision an AI agent on a remote server via SSH.

    Steps:
    1. SSH into target server
    2. Auto-detect OS
    3. Install Docker if not present
    4. Generate unique agent ID + API key
    5. Write agent config file
    6. Start agent container
    7. Verify health
    8. Return status

    Args:
        host: Server hostname or IP.
        port: SSH port (default 22).
        username: SSH username.
        password: SSH password.
        agent_id: Unique agent identifier.
        agent_name: Human-readable agent name.
        role: Agent role (worker, supervisor, chat).
        hub_url: URL of the AI One hub for registration.

    Returns:
        Dict with api_key, config, log fields.

    Raises:
        paramiko.AuthenticationException: SSH auth failed.
        ConnectionError: Connection timeout or refused.
        RuntimeError: Provisioning step failed.
    """
    log_lines: list[str] = []
    api_key = f"ak-{uuid.uuid4().hex}"
    config: dict[str, Any] = {
        "agent_id": str(agent_id),
        "agent_name": agent_name,
        "role": role,
        "api_key": api_key,
        "hub_url": hub_url,
    }

    def _log(msg: str) -> None:
        log_lines.append(msg)
        print(f"[Provisioner] {msg}")

    try:
        # 1. SSH Connection
        _log(f"Connecting to {username}@{host}:{port}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: ssh.connect(
                hostname=host,
                port=port,
                username=username,
                password=password,
                timeout=30,
            ),
        )
        _log("SSH connection established.")

        # 2. Detect OS
        _stdin, stdout, _stderr = ssh.exec_command("cat /etc/os-release 2>/dev/null || cat /etc/issue 2>/dev/null || echo unknown")
        os_info = stdout.read().decode().strip()
        _log(f"Detected OS:\n{os_info[:200]}")

        # 3. Check / Install Docker
        _log("Checking Docker installation...")
        _stdin, stdout, _stderr = ssh.exec_command("which docker && docker --version || echo 'DOCKER_NOT_FOUND'")
        docker_check = stdout.read().decode().strip()

        if "DOCKER_NOT_FOUND" in docker_check or not docker_check:
            _log("Docker not found. Installing Docker...")
            _stdin, stdout, _stderr = ssh.exec_command(
                "curl -fsSL https://get.docker.com | sh 2>&1"
            )
            install_out = stdout.read().decode()
            _log(f"Docker install output:\n{install_out[:500]}")
        else:
            _log(f"Docker already installed: {docker_check}")

        # 4. Generate config
        config_content = (
            f"AGENT_ID={agent_id}\n"
            f"AGENT_NAME={agent_name}\n"
            f"ROLE={role}\n"
            f"API_KEY={api_key}\n"
            f"HUB_URL={hub_url}\n"
        )
        remote_config_path = f"/etc/ai-one/{agent_id}.env"

        _log(f"Writing config to {remote_config_path}...")
        ssh.exec_command(f"mkdir -p /etc/ai-one")
        with ssh.open_sftp() as sftp:
            with sftp.open(remote_config_path, "w") as f:
                f.write(config_content)
        _log("Config written.")

        # 5. Start agent container (mock for now — real image comes later)
        _log("Pulling agent image...")
        _stdin, stdout, _stderr = ssh.exec_command(
            f"docker pull alpine:latest 2>&1 && "
            f"docker run -d --name ai-one-{agent_id.hex[:8]} "
            f"--restart unless-stopped "
            f"-e AGENT_ID={agent_id} "
            f"-e AGENT_NAME={agent_name} "
            f"-e ROLE={role} "
            f"-e API_KEY={api_key} "
            f"-e HUB_URL={hub_url} "
            f"alpine:latest sleep infinity"
        )
        container_out = stdout.read().decode().strip()
        _log(f"Container started: {container_out[:100]}")

        # 6. Verify health
        _stdin, stdout, _stderr = ssh.exec_command(
            f"docker ps --filter name=ai-one-{agent_id.hex[:8]} --format '{{{{.Status}}}}'"
        )
        health_status = stdout.read().decode().strip()
        _log(f"Container health: {health_status}")

        # 7. Register agent (curl to hub)
        _log("Registering agent with AI One hub...")
        _stdin, stdout, _stderr = ssh.exec_command(
            f"curl -s -X POST {hub_url}/api/agents/ "
            f"-H 'Content-Type: application/json' "
            f"-d '{{\"name\": \"{agent_name}\", \"host\": \"{host}\", \"role\": \"{role}\", \"config\": {{\"deployed\": true}}}}' "
            f"2>&1 || echo 'Registration skipped (hub may be unreachable)'"
        )
        register_out = stdout.read().decode().strip()
        _log(f"Registration: {register_out[:200]}")

        ssh.close()

    except paramiko.AuthenticationException as e:
        _log(f"SSH Authentication failed: {e}")
        raise
    except socket.timeout as e:
        _log(f"SSH Connection timed out: {e}")
        raise ConnectionError(f"SSH connection to {host}:{port} timed out") from e
    except Exception as e:
        _log(f"Provisioning error: {e}")
        raise RuntimeError(f"Provisioning failed: {e}") from e

    return {
        "api_key": api_key,
        "config": config,
        "log": "\n".join(log_lines),
    }
