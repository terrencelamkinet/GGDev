const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('smartAI', {
  // Window
  minimize: function() { ipcRenderer.send('minimize'); },
  close: function() { ipcRenderer.send('close'); },

  // System
  getSysInfo: function() { return ipcRenderer.invoke('getSysInfo'); },
  getWeather: function() { return ipcRenderer.invoke('getWeather'); },

  // Chat
  chat: function(msg) { return ipcRenderer.invoke('chat', msg); },

  // Notes
  getNotes: function() { return ipcRenderer.invoke('getNotes'); },
  saveNote: function(note) { return ipcRenderer.invoke('saveNote', note); },
  deleteNote: function(idx) { return ipcRenderer.invoke('deleteNote', idx); },

  // Recording
  saveRecording: function(b64) { return ipcRenderer.invoke('saveRecording', b64); },

  // Config
  getConfig: function(key) { return ipcRenderer.invoke('getConfig', key); },

  // Notifications
  onToggle: function(cb) { ipcRenderer.on('toggle', cb); },
});
