# Focus Bird × 專注力科學 — 完整 AI 圖像生成 Prompt 指引
## Lenovo ThinkPad X1 Carbon OLED 2880×1800 優化版
---
## 一、科學依據：用色對專注力的影響
在制定任何視覺設計前，必須先理解權威研究的結論。以下是兩項核心研究的發現：
### 研究一：Xia et al., 2022 — Brain Sciences（PMC8774152）
對70名參與者進行七種背景色下的認知心理測試，涵蓋邏輯思維、側向思維及細節注意力：[^1]

| 顏色 | 整體認知 | 邏輯思維 | 注意細節 | 評分方向 |
|------|---------|---------|---------|---------|
| **綠色** | ⭐ 最佳 — 最快回應、最低錯誤率 | High Arousal | High Arousal (最佳) | ✅ 強烈推薦 |
| **藍色** | 中高 — 較佳邏輯 | Low Impulsiveness (穩定) | Low Arousal | ✅ 次選 |
| **橙色** | 中 — 側向思維刺激 | Low Arousal (差) | Low Arousal | ⚠️ 限量使用 |
| **紫色** | 最差 — 最慢、最多錯誤 | Worst | Worst | ❌ 避免 |

**關鍵結論**：綠色在現實環境下是促進認知能力最穩定的顏色，跨所有認知任務均表現最佳。[^1]
### 研究二：Soltanzadeh et al., 2024 — Brain and Behavior（PMC11410860）
用 EEG + VR 測量不同顏色和亮度對「持續注意力」及「走神（Mind Wandering）」的影響：[^2]

| 條件 | 持續注意力 | 走神網絡活動 | 結論 |
|------|---------|------------|------|
| 藍色 + 高亮度 | ✅ 顯著提升（p<0.003）| ✅ 顯著減少 | 最佳持續專注條件 |
| 白色 + 高亮度 | ❌ 無改善 | ❌ 走神增加 | 避免純白背景 |
| 藍色 + 低亮度 | ❌ 無顯著改善 | 中性 | 亮度同樣關鍵 |

**關鍵結論**：高亮度藍色（特別結合螢幕本身的亮度）是改善持續注意力（sustained attention）最有效的顏色條件，能減少走神相關腦區的活動。[^2]
### 研究三：嚴肅遊戲設計藍圖（PMC8050194）
針對注意力訓練遊戲設計的研究指出，視覺刺激必須：[^3]
- 觸發情感狀態以引導注意力（emotions direct attention）
- 使用**較低飽和度的形狀和顏色**，避免過度刺激（therapists should select "less saturated" elements）
- 提供即時回饋但不製造過量干擾
### Lenovo X1 Carbon 螢幕規格
遊戲運行於 Lenovo ThinkPad X1 Carbon Gen 12，這對用色有直接影響：[^4][^5]
- **螢幕**：14吋 OLED，2880×1800，120Hz，100% DCI-P3 色域
- **亮度**：最高 400 nits，HDR 500 認證
- **特性**：OLED 黑位極深，色彩飽和度遠超普通 IPS 面板

> ⚠️ **OLED 特別警告**：OLED 螢幕上的鮮豔橙色（#F4A261）和飽和紅色在高亮度下會造成視覺疲勞；研究亦顯示走神增加。Focus Bird 作為**專注訓練工具**，需嚴格控制橙色的使用範圍。

***
## 二、修訂後的「專注力優先」色彩系統
基於以上研究，對原有「綠橙」Canva 風格作出科學修訂：
### 修訂版色盤（Focus-Science Palette）
```
主焦點色（Green — 促進認知 + 細節注意力）:
  深青綠    #1a6b5a   ← 背景主色、地面（低飽和、護眼）
  中青綠    #2EC4B6   ← 主角鳥、按鈕、互動元素（清醒感）
  淺薄荷    #A8DADC   ← 天空、卡片背景（calm + focus）

持續注意色（Blue — 減少走神）:
  深藍      #1a3a5c   ← 夜空遠景、深層背景（高亮度 OLED 表現佳）
  亮藍      #4361EE   ← 專注光環、Focus Bar 滿格狀態
  天藍      #74B3CE   ← 中景、河流、雲影

獎勵色（Amber/Orange — 僅限短暫反饋，< 15% 畫面佔比）:
  深琥珀    #E8933A   ← 金幣、高分特效（限 < 3 秒出現）
  淺橙      #FFCB77   ← 嘴喙、金幣光暈（小面積點綴）

中性基底:
  奶白      #F4F9F9   ← 卡片、HUD 文字背景（非純白，避免走神）
  深灰藍    #264653   ← 所有文字（高對比不刺眼）
```

**顏色比例原則（專注訓練黃金比例）**：
- 🟢 綠/青綠系：55% — 主要視覺佔比
- 🔵 藍色系：25% — 輔助深度
- 🟡 琥珀/橙系：≤ 10% — 獎勵瞬間
- ⚪ 中性色：10% — UI/文字

***
## 三、動畫設計原則（減少干擾、強化專注反饋）
基於認知負荷理論及動畫速度對認知表現的研究：[^6][^7][^8]
### 核心動畫規則
| 規則 | 科學依據 | 具體數值 |
|------|---------|---------|
| **背景 Parallax 速度要慢** | 快速背景動作佔用視覺注意力資源[^6] | 遠景 0.1x、中景 0.3x、前景 1x |
| **角色動畫幀率要流暢** | 120Hz OLED 螢幕下 60fps 動畫更沉浸[^4] | 最少 6 幀翅膀循環 |
| **反饋動畫要短而明確** | 過長動畫打斷 Flow 狀態[^7] | 收集特效 < 0.3 秒 |
| **避免閃爍元素** | 閃爍增加焦慮感、破壞持續注意力[^2] | 任何閃爍間隔 > 1 秒 |
| **Focus Bar 動畫要平滑** | 平滑狀態變化提供持續感知反饋[^3] | CSS transition 0.3s ease |
| **Game Over/Level Up 動畫要 Ease-Out** | 向外彈出的減速動畫比線性或彈入更不刺激[^7] | scale 0.8→1.0, duration 0.4s |

***
## 四、完整 AI 圖像生成 Prompt（逐元素）
以下所有 prompt 使用統一風格基底。將此 **STYLE BASE** 附加在每條 prompt 末尾：

```
STYLE BASE:
flat vector illustration, clean modern cartoon game art, soft rounded shapes,
subtle 1-2px outline, minimal shading, single soft drop shadow only,
calm teal-blue-green dominant palette with amber accent max 10% area,
focus-training game aesthetic, low visual noise, no busy patterns,
designed for OLED display with deep blacks, high resolution 2x PNG,
transparent background unless stated, absolutely no text in image
```

***
### Prompt 1：三層視差背景（Three Parallax Layers）
**科學依據**：分層靜態感強的背景減少視覺干擾，保留主體鳥和金幣的視覺優先度。[^6]

#### Layer 1 — 天空（最慢移動，速度係數 0.1x）

```
A 2D game sky background, 400×500px portrait, for an OLED display game.
Sky gradient from deep navy-teal (#1a3a5c) at the very top, transitioning 
smoothly to soft teal (#A8DADC) at the mid-horizon, then to very pale 
mint-white (#F4F9F9) near the bottom edge.
A single soft amber sun (top-right corner, radius ~30px) with a diffuse 
warm glow (3 layers of opacity: 40%, 20%, 8%). No hard sun rays.
Two to three soft cloud shapes: white with subtle teal shadows, rounded 
pillowy shapes only, NO sharp edges. Clouds should look calm and unhurried.
Overall brightness: medium — not too dark, not too bright. OLED-optimized.

STYLE BASE: flat vector illustration, clean modern cartoon game art, soft 
rounded shapes, subtle 1-2px outline, minimal shading, single soft drop 
shadow only, calm teal-blue-green dominant palette with amber accent max 
10% area, focus-training game aesthetic, low visual noise, no busy patterns,
designed for OLED display with deep blacks, high resolution 2x PNG, 
transparent background unless stated, absolutely no text in image
```

#### Layer 2 — 中景山脈（中速，速度係數 0.3x）

```
A 2D game middle-ground parallax layer, 400×160px, PNG with transparent 
top (sky area). Two overlapping smooth rounded hills in deep teal-green 
(#1a6b5a front, #2EC4B6 back). Bezier smooth curves only — no zigzag or 
sharp mountain peaks. One minimalist lollipop-style tree on the left hill 
(circle top, thin stem, all in #1a6b5a slightly lighter shade). Subtle 
teal-amber gradient along the hilltops (warm morning light effect, 
very subtle — 15% opacity amber overlay at ridge only). 
No buildings, no busy detail. Clean and calm.

STYLE BASE: [see above]
```

#### Layer 3 — 前景草地（正常速度，速度係數 1x，seamless horizontal tile）

```
A 2D game foreground ground strip, 400×55px, seamless horizontal tile, 
PNG with transparent top. Thick grass ground in bright-medium teal-green 
(#2EC4B6 base, #1a6b5a shadow at base). 10-12 grass blades of varying 
height (6-12px), smooth curved tips, not sharp. 
4-5 tiny simplified flowers: alternating amber (#FFCB77) and pale teal 
petals, with a small white center dot. NO flowers taller than 10px — keep 
very subtle. Bottom edge: a thin translucent teal-blue river strip 
(rgba(116,179,206,0.4)), 8px height only. 
Tile must seamlessly repeat left-to-right without visible seam.

STYLE BASE: [see above]
```

***
### Prompt 2：主角鳥（主科學修訂元素）
**科學依據**：主角使用綠色主體可持續維持用家的 High Arousal 認知狀態；眼睛和嘴喙的琥珀色作為焦點錨點（focal anchor），引導視線集中。[^1]

#### 靜態主角鳥

```
A cute round 2D game bird character for focus training, 64×64px, 
side-view facing right. 

Body: Round chubby oval shape in deep teal (#2EC4B6) with a lighter 
mint-teal (#A8DADC) belly patch (lower 40% of body).
Wings: Short, slightly darker teal (#1a9b8a), tucked at body sides, 
rounded wingtip shapes.
Head: Slightly larger circle attached at right of body, same teal color.
Eye: Large expressive eye — white sclera (70% of eye area), medium-dark 
round pupil (#264653), single bright white highlight dot (top-left of pupil). 
Eye proportions: wide and alert, not droopy.
Beak: Bright amber (#F4A261) small triangle pointing right, clean geometric.
Feet: Two small amber rounded stubs below body, barely visible.
Head crest: A single small amber teardrop-shaped leaf crest on top of head.
Cheek blush: Soft pale amber ellipse on cheek, very subtle (15% opacity).
No outline on the main body — shapes defined by color contrast only.
Transparent background, centered in frame.

STYLE BASE: flat vector illustration, clean modern cartoon game art, soft 
rounded shapes, subtle 1-2px outline, minimal shading, single soft drop 
shadow only, calm teal-blue-green dominant palette with amber accent max 
10% area, focus-training game aesthetic, low visual noise, no busy patterns,
designed for OLED display with deep blacks, high resolution 2x PNG, 
transparent background unless stated, absolutely no text in image
```

#### 4幀 Sprite Sheet（動畫）

```
A 4-frame horizontal sprite sheet for a 2D bird character, 
total 256×64px (each frame 64×64px). Same teal-green round bird facing right.

Frame 1 (IDLE): Wings at neutral side position, eye relaxed but alert, 
subtle shadow beneath body. Body perfectly round.

Frame 2 (FLAP UP — dive command): Wings raised upward 40°, beak slightly 
open showing effort, eye slightly wider, body compressed slightly vertically 
(squash effect), tiny speed lines at wing tips (2-3 short lines, teal color).

Frame 3 (FLOAT UP): Wings in horizontal spread, body slightly elongated 
upward (stretch effect), eyes normal, tail feathers spread slightly.

Frame 4 (GLIDE): Wings swept back 20°, body elongated slightly forward 
(elongation effect), eyes focused/narrowed slightly, a soft teal motion 
trail behind (3px wide, fading to transparent over 15px).

Frames separated by 1px white guide lines. Consistent character identity 
across all 4 frames. Transparent background.

STYLE BASE: [see above]
```

#### 受傷狀態鳥（Game Over）

```
Same teal round bird character, 64×64px, expressing dizzy/hurt state.
Eyes replaced with small "×" symbols in dark color (#264653).
Body color slightly desaturated/grey-shifted (reduce saturation by 40%).
Wings drooping downward at 30°.
3 small amber stars (★) floating around the head at 12, 2, and 9 o'clock 
positions, each star rotated differently.
A small teal impact burst (5-6 short radiating lines, 6px long each) at 
left edge of body suggesting collision point.
Body silhouette same as idle, only expression and wing position change.
Transparent background.

STYLE BASE: [see above]
```

***
### Prompt 3：金幣（限制使用，純獎勵功能）
**科學依據**：橙/金色作為獎勵色，應集中在金幣這一個元素上，在其他地方避免使用，以保持獎勵信號的清晰度。[^3]

```
A single collectible gold coin for a 2D focus training game, 32×32px.
Round coin shape, amber-gold gradient fill (center #FFCB77, edge #E8933A).
Dark teal outline (1.5px, #264653) around the coin edge.
Center symbol: a small simplified leaf/checkmark shape in deep teal 
(#1a6b5a), 40% of coin diameter, suggesting nature/growth.
A single white arc highlight (crescent, 25% opacity, upper-left quadrant) 
suggesting 3D sheen without photorealism.
Soft amber glow (rgba(232,147,58,0.35)) radiating 4px beyond coin edge — 
subtle, not overwhelming.
NO multiple sparkles or stars around it — keep the coin itself as the 
focus point.
Transparent background.

STYLE BASE: [see above]
```

***
### Prompt 4：UI 按鈕（深青綠 CTA，取代橙色按鈕）
**科學依據**：按鈕改用青綠色（而非橙色）減少整體橙色面積佔比，保持 ≤10% 的獎勵色原則。[^1][^2]

#### 主要 CTA 按鈕（開始 / 下一關）

```
A UI button graphic for a focus-training game, 200×56px, no text.
Large rounded rectangle (radius 14px) with deep teal gradient fill 
(left to right: #2EC4B6 to #1a9b8a). Dark teal outline (2px, #1a6b5a).
Inner highlight: thin white semi-transparent arc along the top edge 
(20% opacity, 2px, full width).
Soft drop shadow below: (0px 4px 12px rgba(30,107,90,0.4)).
Slight "pillow" feel from the top highlight and bottom shadow.
Button should feel calm and approachable — NOT alarming or urgent.
Transparent background.

STYLE BASE: [see above]
```

#### 次要按鈕（主頁 / 重試）

```
Same 200×56px button, secondary style.
Fill: very pale teal (#F4F9F9), outline (#2EC4B6, 1.5px).
Drop shadow: (0px 2px 8px rgba(46,196,182,0.2)).
Lower visual weight than primary button.
Transparent background.

STYLE BASE: [see above]
```

***
### Prompt 5：HUD 分數卡片
**科學依據**：奶白（非純白）背景卡片避免因強對比白色造成視覺疲勞；OLED 螢幕上純白會顯著增加亮度。[^5][^2]

```
A score badge/card for a 2D game HUD, 170×44px.
Rounded pill shape (radius 22px), fill: very pale teal-white (#F4F9F9), 
dark teal outline (#2EC4B6, 1.5px).
Drop shadow: (0px 2px 8px rgba(46,196,182,0.25)).
Left section (30px wide): small gold coin icon — same style as Prompt 3, 
24px diameter, no glow at this scale.
Right section (30px wide): tiny amber 5-pointed star icon, 16px.
Center: blank space for dynamic score number text (will be added by CSS).
Overall: calm and non-intrusive — should not distract from gameplay.
Transparent background.

STYLE BASE: [see above]
```

***
### Prompt 6：專注力量條 (Focus Bar) 三種狀態圖示
**科學依據**：Focus Bar 是遊戲的核心生理反饋元素，視覺顏色需直接對應專注程度，使用研究驗證的顏色。[^1][^2]

```
Three horizontal Focus Bar fill states on a single 320×100px reference 
sheet, stacked vertically, each bar 260×18px with rounded ends.

Bar 1 (LOW focus, 25% width): gradient fill from #E76F51 (warm red-orange) 
to #E8933A (amber). Subtle inner glow.

Bar 2 (MEDIUM focus, 60% width): gradient fill from #2EC4B6 (teal) to 
#74B3CE (sky blue). Clean and stable-looking.

Bar 3 (HIGH focus, 95% width): gradient fill from #4361EE (bright blue) 
to #2EC4B6 (teal). Outer glow aura (rgba(67,97,238,0.4), 4px blur).

Each bar on a dark (#264653) rounded-rect container (1.5px track).
Bars labeled LOW / MED / HIGH in small white annotation text to the right.
Dark navy background (#1a1a2e).

STYLE BASE: [see above]
```

***
### Prompt 7：過關 / Game Over 卡片
**科學依據**：覆蓋畫面採用奶白卡片（非純黑 overlay），降低突然轉換的視覺衝擊；標題條用深青綠而非橙色。[^6]

#### 過關卡 (Level Complete)

```
A "Level Complete" popup panel for a 2D focus training game, 320×380px.
Large rounded rectangle card, fill: #F4F9F9 (pale teal-white), 
border: 2px solid #2EC4B6, corner radius 20px.
Top section (60px tall, full width): deep teal header bar (#1a6b5a), 
rounded top corners matching card. Header space is blank (text added by JS).
Below header: a single amber 5-pointed star badge (center aligned, 48px), 
flanked by two smaller amber stars (32px each). Subtle star glow.
Middle content area (blank space with light horizontal divider line).
Bottom section: two button placeholder shapes side by side (primary teal, 
secondary cream, both 130×44px).
Right edge decoration: the same teal round bird character (32px, idle pose, 
happy version with eyes curving upward), peeking in from the right side.
Transparent background.

STYLE BASE: [see above]
```

#### Game Over 卡

```
Same 320×320px popup panel. Dark header bar (#264653 — darker/moodier 
than level complete). Star replaced with a single amber circle with a "×" 
inside. Bird character at right edge: hurt/dizzy pose (from Prompt 2). 
Three small amber stars floating around the bird.
Same button layout. Same teal card border.
Transparent background.

STYLE BASE: [see above]
```

***
### Prompt 8：收集特效 VFX Sprite Sheet
**科學依據**：獎勵特效時長 < 0.3s、面積小，確保不打斷 Flow 狀態。[^7][^3]

```
A 5-frame coin-collect VFX sprite sheet, each frame 48×48px (total 240×48px).

Frame 1: A small amber glow circle (12px radius, 60% opacity).
Frame 2: Circle expands (18px), 6 short radiating teal lines (8px each).
Frame 3: 4 small amber 4-pointed stars scatter outward (8px each), 
central white flash (6px, 80% opacity).
Frame 4: Stars fading (40% opacity), lines shorter (4px).
Frame 5: Nearly transparent — just 2-3 tiny dots fading.

Colors: amber (#F4A261) and teal (#2EC4B6) and white only. No red, no orange.
Total animation designed to last 0.25 seconds at 20fps.
Frames separated by 1px white lines. Transparent background.

STYLE BASE: [see above]
```

***
### Prompt 9：專注光環（Focus Aura） — 高專注狀態
**科學依據**：使用研究驗證的藍色（bright blue）作為「高度專注」的視覺回饋色；替換原有的藍色 `rgba(72,219,251)` 為更接近研究最佳條件的深亮藍。[^2]

```
A circular focus aura effect, 80×80px, centered on transparent background.
This is a HIGH FOCUS state indicator for a focus training game.

Center: transparent (bird will be underneath).
Ring 1 (radius 32px): Soft teal (#2EC4B6) dashed ring, 1.5px, 6 dashes.
Ring 2 (radius 38px): Bright blue (#4361EE), 1px, 8 dashes, rotated 22° 
from Ring 1.
Radial glow: Soft blue (#4361EE, 20% opacity) radiating from center to 
edge, with deepest intensity at edge, fading at center.
4 tiny 4-pointed white sparkles at N, E, S, W positions (6px each).
The aura should suggest calm focused energy, NOT excitement or danger.

STYLE BASE: [see above]
```

***
## 五、動畫實施建議（給 HTML/Canvas 代碼修改參考）
以下是針對 Lenovo X1 Carbon 120Hz OLED 螢幕的動畫優化建議，與 Prompt 設計配合：
### 背景 Parallax
```javascript
// 三層速度比例（X1 Carbon 120Hz，60fps target）
const BG_SPEEDS = {
  sky:    0,      // 靜態 — 天空不動，降低干擾
  hills:  0.15,   // 極慢 — 遠山微微飄移
  ground: 1.0     // 正常 — 草地與現有速度一致
};
```
### 鳥的角度傾斜（更自然）
```javascript
// 現有: angle = Math.max(-0.3, Math.min(0.3, b.vy * 0.04))
// 修改為更柔和的角度，配合 OLED 高刷感知
const angle = Math.max(-0.25, Math.min(0.25, b.vy * 0.025));
// 增加緩衝 easing
b.displayAngle = b.displayAngle * 0.85 + angle * 0.15; // smooth lerp
```
### 收集金幣特效時長控制
```javascript
// 每個特效最多存在 18 幀 (0.3s at 60fps)
// 超過 18 幀自動移除，避免畫面過於繁忙
if (effect.frame > 18) effects.splice(i, 1);
```
### Focus Bar CSS 動畫
```css
/* 替換現有 transition: width 0.15s */
#focusBar {
  transition: width 0.3s ease, background 0.5s ease;
  /* 顏色隨專注度動態變化 */
}
/* Low focus */
.focus-low  { background: linear-gradient(90deg, #E76F51, #E8933A); }
/* Mid focus */
.focus-mid  { background: linear-gradient(90deg, #2EC4B6, #74B3CE); }
/* High focus */
.focus-high { background: linear-gradient(90deg, #4361EE, #2EC4B6); 
              box-shadow: 0 0 8px rgba(67,97,238,0.5); }
```

***
## 六、設計元素快速索引
| 素材 | 尺寸 | Prompt 號碼 | 主色 | 用途 |
|------|------|-----------|------|------|
| 天空背景 | 400×500 | Prompt 1a | #1a3a5c→#A8DADC | 靜止 Layer |
| 中景山脈 | 400×160 | Prompt 1b | #1a6b5a | 0.15x 速度 |
| 前景草地 | 400×55 (tile) | Prompt 1c | #2EC4B6 | 1x 速度 |
| 主角鳥（靜）| 64×64 | Prompt 2a | #2EC4B6 + #F4A261 | 主角 |
| 主角 Sprite Sheet | 256×64 | Prompt 2b | 同上 | 動畫幀 |
| 受傷狀態鳥 | 64×64 | Prompt 2c | 去飽和 + × 眼 | Game Over |
| 金幣 | 32×32 | Prompt 3 | #FFCB77 + #1a6b5a | 獎勵 |
| 主 CTA 按鈕 | 200×56 | Prompt 4a | #2EC4B6 | 開始/繼續 |
| 次要按鈕 | 200×56 | Prompt 4b | #F4F9F9 | 主頁/取消 |
| 分數卡片 | 170×44 | Prompt 5 | #F4F9F9 + #2EC4B6 | HUD |
| Focus Bar 狀態 | 320×100 | Prompt 6 | 三色系統 | 生理反饋 |
| 過關 Popup | 320×380 | Prompt 7a | #F4F9F9 + #1a6b5a | 完關 |
| Game Over Popup | 320×320 | Prompt 7b | #F4F9F9 + #264653 | 遊戲結束 |
| 收集特效 VFX | 240×48 | Prompt 8 | #F4A261 + #2EC4B6 | 金幣回饋 |
| 專注光環（高）| 80×80 | Prompt 9 | #4361EE + #2EC4B6 | 高專注狀態 |

***
## 七、與原設計的關鍵修訂對比
| 元素 | 原設計 | 修訂後 | 科學依據 |
|------|--------|--------|---------|
| 主色調 | 綠＋橙（Canva 風格） | 青綠＋深藍（專注優先） | 綠色最佳認知；藍色減走神[^1][^2] |
| 主角鳥顏色 | 棕紅 `#e17055` | 深青綠 `#2EC4B6` | 增加主角的「注意力錨點」效果 |
| 按鈕顏色 | 藍色 `#48dbfb` / Canva 橙 | 深青綠 `#2EC4B6` | 統一配色，避免多色干擾[^6] |
| 橙色使用 | 大量（Canva 模板風格）| 嚴格限制 ≤10%（僅金幣）| OLED 高飽和橙刺激走神[^2] |
| Focus Bar | 彩虹漸層 | 三階段 橙→青→藍 | 直接映射認知研究的「最佳色」[^1][^2] |
| Game Over overlay | 純黑半透明 | 奶白卡片＋深青綠標題 | 降低突然視覺衝擊[^6] |
| 背景 | 單純 Canvas 繪製 | 三層 PNG，深藍天空 | OLED 深黑顯示極佳，減少走神[^2] |
| Parallax 天空 | 移動 | 靜止 | 減少無關動作佔用視覺注意資源[^6] |

---

## References

1. [A Comparative Study of Colour Effects on Cognitive Performance in ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC8774152/) - This research explores the influence of colour on cognitive performance and intellectual abilities (...

2. [Color and brightness at work: Shedding some light on mind ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC11410860/) - Brain Behav. 2024 Sep 18;14(9):e70020. doi: 10.1002/brb3.70020

3. [A serious-gamification blueprint towards a normalized attention - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8050194/) - This paper, therefore, introduces a generic reference model that guides in the design of proper trea...

4. [ThinkPad X1 Carbon Redesigned for 2024](https://www.bestlaptop.deals/articles/2024-thinkpad-x1-carbon-review) - It is bright at over 400 nits and has a wide color gamut. It has a high resolution of 2880x1800 pixe...

5. [Lenovo ThinkPad X1 Carbon Gen 12 - Review 2024](https://me.pcmag.com/en/laptops/22392/lenovo-thinkpad-x1-carbon-gen-12) - Lenovo ThinkPad X1 Carbon Gen 12 Specs ; Native Display Resolution, 2880 by 1800 ; Operating System,...

6. [How Visual Elements Guide User Attention in Modern Games](https://www.ruislipblinds.co.uk/how-visual-elements-guide-user-attention-in-modern-games/) - Movement naturally attracts human attention, which game designers exploit through animations, visual...

7. [Figma + Rive: sharing my workflow for UI animations | by Andrei Rybin](https://uxdesign.cc/how-i-create-animation-for-interfaces-7183b3b6482f) - Tools and methods I use for interface animations, including Rive. We'll also review an older project...

8. [Effects of animation's speed of presentation on perceptual ...](https://www.sciencedirect.com/science/article/abs/pii/S0959475209000243) - Furthermore, animations can help learners to mentally visualise a process or procedure, thus reducin...

