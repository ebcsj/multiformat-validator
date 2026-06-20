# MultiFormat Validator CLI

專業級多格式語法靜態掃描與驗證工具，支援 63 種檔案格式、5 種介面語言。

[查看更新紀錄](CHANGELOG.md)

> **本項目已完全開源！** 目前已有學校與我們聯繫，表達希望將此工具投入教育用途。為了提供更完善的體驗，我們正積極籌備並開發更多新功能，敬請期待！

## 授權條款

Copyright (c) 2026 MultiFormat Validator CLI - Kerby Chow. All rights reserved.

- **允許：** 個人、非商業、教育用途；允許修改與建立衍生作品（僅限個人使用）
- **禁止：** 商業用途、再散布、販售
- **分享：** 僅限官方 GitHub 連結

完整授權條款：[LICENSE](LICENSE)

## 為什麼需要這個工具？

開發者經常需要檢查不同格式檔案的語法是否正確。MultiFormat Validator CLI 讓你：

- 一次驗證 JSON、Python、HTML、XML、BAT/CMD 等 63 種格式
- 使用熟悉的終端機介面操作
- 匯出專業的 HTML 診斷報告

## 功能特色

| 功能 | 說明 |
|------|------|
| 多語言介面 | 繁體中文、简体中文、English、日本語、한국어 |
| 63 種格式 | JSON、Python、HTML、XML、PHP、CSS、Markdown 等 |
| 批次掃描 | 遞迴掃描整個資料夾（使用串流產生器） |
| 匯出報告 | HTML、JSON、CSV、TXT 報告格式，可自選儲存路徑 |
| 智慧編碼 | 自動偵測 UTF-8、GBK、Big5 等編碼 |
| 歷史紀錄 | 自動儲存上次驗證的檔案路徑 |
| 自動修復 | 支援基礎語法自動修復（含差異預覽） |
| 自訂規則 | 自定義驗證規則（正則表達式，含 ReDoS 防護） |
| 插件系統 | 支援載入第三方驗證器（含路徑驗證與哈希校驗） |
| 右鍵選單 | 在 Windows 檔案總管中直接驗證檔案 |
| 主題切換 | 深色與淺色主題，即時切換 |
| 檔案瀏覽器 | 互動式瀏覽器，支援直接輸入路徑 |
| 錯誤偵測 | 清楚的空白檔案、找不到檔案、編碼錯誤訊息 |
| 安全防護 | 沙箱化驗證器、XXE 防護、路徑保護、執行緒安全 |
| 日誌輪替 | 自動日誌檔案輪替（最大 5MB，保留 3 個備份） |
| 設定驗證 | 自動驗證設定值的類型與範圍 |

## 安裝需求

| 需求 | 版本 |
|------|------|
| Python | 3.12 或以上 |
| colorama | >= 0.4.6 |
| pyyaml | （可選）用於 YAML 驗證 |

## 安裝方式

### 最簡單的方式（推薦新手）

1. 下載這個專案（Download ZIP）
2. 打開專案資料夾
3. 雙擊 `install.bat`
4. 選擇 `[1] Install`，等待安裝完成
5. 完成！在終端機輸入 `check-cli` 即可開始使用

### 方式二：手動安裝

```bash
# 1. 複製專案
git clone <repo-url>
cd "CLI Making"

# 2. 安裝套件
pip install -e .

# 3. 驗證安裝
check-cli --version
```

### 方式三：不修改 PATH

```bash
# 直接在專案目錄執行
check-cli.bat

```

## 使用方式

### 互動模式

```bash
check-cli
```

啟動後選擇語言（1-5），然後使用主選單：

| 選項 | 功能 | 說明 |
|------|------|------|
| `[0]` | 快捷重試 | 重新驗證上次檢查的檔案 |
| `[1]` | 驗證單一檔案 | 輸入檔案路徑進行驗證 |
| `[2]` | 批次掃描 | 遞迴掃描資料夾中的所有檔案 |
| `[3]` | 檔案瀏覽器 | 互動式瀏覽目錄並選取檔案 |
| `[4]` | 比較檔案 | 比較兩個檔案的驗證結果 |
| `[5]` | 批次匯出 | 將掃描結果匯出為 JSON/CSV/TXT/HTML |
| `[6]` | 範本管理 | 儲存/載入/刪除驗證範本 |
| `[7]` | 統計資訊 | 統計行數、註解、空白行 |
| `[8]` | 歷史紀錄 | 查看並管理驗證歷史 |
| `[9]` | 自訂驗證器 | 建立/刪除自訂驗證規則 |
| `[R]` | 自訂規則 | 定義正則表達式驗證規則 |
| `[P]` | 插件管理 | 載入/卸載第三方驗證器插件 |
| `[Q]` | 快速驗證 | 安裝右鍵選單（Windows） |
| `[S]` | 設定 | 變更語言、主題、日誌等 |
| `[H]` | 說明 | 顯示說明和使用資訊 |
| `[X]` | 離開 | 結束程式 |

#### 選項 1：驗證單一檔案

1. 從主選單選擇 `[1]`
2. 貼上檔案路徑（在終端機中右鍵貼上）
3. 查看驗證報告
4. 如有錯誤，可選擇自動修復或匯出 HTML 報告

#### 選項 2：批次掃描資料夾

1. 從主選單選擇 `[2]`
2. 輸入資料夾路徑
3. 一次查看所有檔案結果
4. 可選擇匯出 JSON/CSV/TXT/HTML 報告，並自選儲存路徑

#### 選項 3：檔案瀏覽器

1. 從主選單選擇 `[3]`
2. 輸入數字導航目錄，或輸入完整路徑直接跳轉
3. 選取檔案進行驗證

#### 選項 8：歷史紀錄

1. 從主選單選擇 `[8]`
2. 查看最近的驗證記錄
3. 可選擇匯出或清除歷史

### CLI 參數模式

```bash
check-cli <file>                     # 驗證檔案
check-cli <folder> -r                # 遞迴掃描
check-cli -l zh_TW <file>           # 指定語言
check-cli -f json -o out.json       # 匯出 JSON 報告
check-cli -f csv -o out.csv         # 匯出 CSV 報告
check-cli -f txt -o out.txt         # 匯出 TXT 報告
check-cli -f html -o out.html       # 匯出 HTML 報告
check-cli --list-formats             # 列出所有支援格式
check-cli --version                  # 顯示版本
```

### 互動模式 - 批次匯出

使用批次掃描（選項 `[2]`）時，可以選擇匯出結果：

```
匯出格式 (JSON/CSV/TXT/HTML)：JSON

輸出檔案路徑（留空使用預設位置）：
> C:\Users\YourName\Desktop\my_report.json

  已儲存至：C:\Users\YourName\Desktop\my_report.json
```

- 路徑**留空**會儲存到目前目錄，檔名為 `batch_report.<格式>`
- 輸入**完整路徑**可儲存到任意位置

### CLI 參數說明

| 參數 | 選項 | 說明 |
|------|------|------|
| `path` | — | 檔案或資料夾路徑 |
| `-l, --lang` | `zh_TW`, `zh_CN`, `en`, `ja`, `ko` | 介面語言（預設：en） |
| `-f, --format` | `text`, `json`, `csv`, `txt`, `html` | 輸出格式（預設：text） |
| `-o, --output` | 檔案路徑 | 輸出檔案路徑 |
| `-r, --recursive` | — | 遞迴掃描資料夾 |
| `--list-formats` | — | 列出所有支援格式 |
| `--version` | — | 顯示版本 |

## 設定

設定檔位於 `~/.multiformat_validator/preferences.json`：

```json
{
  "language": "en",
  "output_format": "text",
  "theme": "dark",
  "exclude_patterns": ["node_modules", ".git", "__pycache__", ".venv"],
  "max_file_size_mb": 10,
  "logging_enabled": false,
  "parallel_scanning": false,
  "parallel_workers": 4
}
```

| 設定項 | 預設值 | 說明 |
|--------|--------|------|
| `language` | `"en"` | 介面語言 |
| `output_format` | `"text"` | 輸出格式 |
| `theme` | `"dark"` | 主題風格 |
| `exclude_patterns` | `["node_modules", ...]` | 排除的資料夾 |
| `max_file_size_mb` | `10` | 最大檔案大小（MB） |
| `logging_enabled` | `false` | 是否啟用日誌 |
| `parallel_scanning` | `false` | 是否使用平行掃描 |
| `parallel_workers` | `4` | 平行執行緒數 |

## 專案結構

程式碼採用模組化設計，便於維護：

```
multiformat_validator/
├── cli.py                    # 入口點（<100行）
├── commands/                 # 命令模組
│   ├── __init__.py          # 命令路由
│   ├── validate.py          # 單一檔案驗證
│   ├── batch_scan.py        # 批次掃描資料夾
│   ├── compare.py           # 檔案比較
│   └── export.py            # 批次匯出
├── ui/                       # 使用者介面
│   ├── menus.py             # 互動式選單系統
│   ├── display.py           # 顯示功能
│   └── prompts.py           # 使用者輸入處理
├── config/                   # 設定管理
│   ├── settings.py          # 設定選單
│   └── templates.py         # 範本管理
├── i18n/                     # 國際化（5種語言）
├── validators/               # 25個格式特定驗證器
└── ...                       # 其他模組（掃描器、匯出器等）
```

## 支援格式

### 設定檔

| 格式 | 副檔名 |
|------|--------|
| JSON | `.json` `.ipynb` `.jsonl` `.topojson` `.geojson` |
| YAML | `.yaml` `.yml` |
| INI | `.ini` `.properties` `.conf` `.cfg` `.prefs` `.inf` |
| XML | `.xml` `.xsd` `.rss` `.svg` `.plist` `.config` `.wsdl` |

### 程式語言

| 格式 | 副檔名 |
|------|--------|
| Python | `.py` `.pyw` `.pyi` `.pyx` |
| JavaScript | `.js` `.jsx` |
| TypeScript | `.ts` `.tsx` |
| Java | `.java` |
| C# | `.cs` |
| Go | `.go` |
| Ruby | `.rb` |
| Rust | `.rs` |
| Kotlin | `.kt` |
| Swift | `.swift` |
| Perl | `.pl` `.pm` |
| Lua | `.lua` |
| Scala | `.scala` |

### Web

| 格式 | 副檔名 |
|------|--------|
| HTML | `.html` `.htm` `.xhtml` `.phtml` `.jsp` `.asp` `.aspx` |
| CSS | `.css` `.wxss` |
| PHP | `.php` `.php3` `.php4` `.php5` `.phps` |

### 標記語言

| 格式 | 副檔名 |
|------|--------|
| Markdown | `.md` `.markdown` `.mdown` `.mdwn` `.mkd` `.mkdn` |

### 腳本與資料庫

| 格式 | 副檔名 |
|------|--------|
| BAT/CMD | `.bat` `.cmd` `.nt` |
| SQL | `.sql` |

**共 63 種副檔名**

## 安全防護

MultiFormat Validator CLI 包含以下安全措施：

| 功能 | 說明 |
|------|------|
| 沙箱化驗證器 | 自訂驗證器在受限環境中執行，僅允許安全的內建函式 |
| 靜態程式碼分析 | AST 解析阻止危險操作（import、exec、eval、open） |
| 插件路徑驗證 | 插件必須位於 `~/.multiformat_validator/plugins/` 目錄 |
| 插件哈希校驗 | SHA-256 校驗和偵測插件是否被竄改 |
| 路徑遍歷防護 | 所有檔案路徑經過正規化，系統目錄受到保護 |
| XML XXE 防護 | SAX 解析器，禁用外部實體載入 |
| ReDoS 防護 | 正則表達式匹配限制每行 1000 字元 |
| 自動修復備份 | 修復前自動建立 .bak 備份檔案 |
| 執行緒安全 | 檔案操作使用鎖機制防止競態條件 |
| 優雅錯誤處理 | PermissionError、FileNotFoundError 妥善處理，不會崩潰 |

詳細安全資訊請參閱 [SECURITY.md](SECURITY.md)。

## 故障排除

### 安裝問題

**Q: `check-cli` 指令無法識別？**

`check-cli` 指令安裝在 Python 的 Scripts 資料夾，可能不在 PATH 中。

解決方案 1：重新安裝並加入 PATH
```bash
pip install -e .
```

解決方案 2：直接使用批次檔
```bash
check-cli.bat
```

解決方案 3：將 Scripts 資料夾加入 PATH（PowerShell）
```powershell
$old = [Environment]::GetEnvironmentVariable('Path','User')
[Environment]::SetEnvironmentVariable('Path', $old + ';C:\Users\YourName\AppData\Local\Python\pythoncore-3.14-64\Scripts','User')
```
然後重新開啟終端機。

**Q: 找不到 `pip` 指令？**

確定 Python 已安裝並加入 PATH：
```bash
python --version
```
如果找不到，請從 https://www.python.org/downloads/ 下載 Python，安裝時勾選「Add Python to PATH」。

**Q: `install.bat` 開啟後立即關閉？**

這通常表示 Python 未安裝。請先安裝 Python 3.12+，然後重新執行 `install.bat`。

### 使用問題

**Q: 路徑包含空格怎麼辦？**

直接貼上即可，系統會自動處理引號：

```
> "C:\Program Files\config.json"
```

不要使用滑鼠拖放檔案到終端機，這可能導致路徑格式問題。請使用右鍵貼上。

**Q: 出現編碼錯誤或亂碼？**

系統支援自動編碼偵測（UTF-8、GBK、Big5 等）。若仍有問題：
1. 用文字編輯器開啟檔案
2. 另存為 UTF-8 編碼
3. 重新嘗試驗證

**Q: 出現「找不到檔案」錯誤？**

請確認：
1. 使用完整絕對路徑（例如 `C:\Projects\file.json`）
2. 包含副檔名
3. 使用正斜線或跳過的反斜線

**Q: 如何在掃描時排除特定資料夾？**

編輯 `~/.multiformat_validator/preferences.json`：

```json
{
  "exclude_patterns": ["node_modules", ".git", "__pycache__", "vendor", "dist"]
}
```

**Q: 出現「檔案太大」錯誤？**

預設最大大小為 10 MB。若要增加：
```json
{
  "max_file_size_mb": 50
}
```

**Q: 如何變更預設語言？**

編輯 `~/.multiformat_validator/preferences.json`：
```json
{
  "language": "zh_TW"
}
```
可用選項：`zh_TW`、`zh_CN`、`en`、`ja`、`ko`

**Q: 如何變更主題？**

編輯 `~/.multiformat_validator/preferences.json`：
```json
{
  "theme": "light"
}
```

### 報告問題

**Q: HTML 報告沒有樣式？**

CSS 完整內嵌在 HTML 檔案中。請使用現代瀏覽器（Chrome / Firefox / Edge）開啟。報告儲存在受檢檔案的同目錄下。

**Q: 如何匯出報告？**

驗證過程中會提示匯出。或使用 CLI：
```bash
check-cli file.py -f json -o report.json
check-cli file.py -f csv -o report.csv
check-cli file.py -f txt -o report.txt
check-cli file.py -f html -o report.html
```

### 效能問題

**Q: 掃描速度很慢？**

對於大型資料夾，啟用平行掃描：
```json
{
  "parallel_scanning": true,
  "parallel_workers": 4
}
```

**Q: 如何啟用日誌？**

編輯 `~/.multiformat_validator/preferences.json`：
```json
{
  "logging_enabled": true,
  "log_path": "validation.log"
}
```

### 其他問題

**Q: 如何重設所有設定？**

刪除設定檔或重設它：
```bash
# 刪除設定檔
rm ~/.multiformat_validator/preferences.json

# 或使用工具中的設定選單
# 選擇 [S] 設定 > [C] 設定 > [7] 重設
```

**Q: 如何查看驗證歷史？**

從主選單選擇 `[8]`，或找到歷史檔案：
```
~/.multiformat_validator/.validation_history.json
```

**Q: 如何解除安裝？**

```bash
pip uninstall multiformat-validator
```
然後刪除專案資料夾。

