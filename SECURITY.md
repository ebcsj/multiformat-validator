# Security Policy / 安全政策

## Supported Versions / 支援版本

| Version | Supported          |
| ------- | ------------------ |
| 3.0.x   | :white_check_mark: |
| < 3.0   | :x:                |

---

## English

### Security Features of This Project

MultiFormat Validator CLI includes the following security measures:

#### 1. Custom Validators (exec() Sandboxing)

- **Static Analysis**: All custom validator code is parsed with `ast.parse()` before execution
- **Blocked Operations**: `import`, `__import__`, `exec`, `eval`, `open`, `compile` are forbidden
- **Restricted Builtins**: Only safe functions (print, len, range, str, int, etc.) are available
- **Module Protection**: Access to `os`, `sys`, `shutil`, `subprocess` is blocked

#### 2. Plugin System (Secure Loading)

- **Path Validation**: Plugins must reside in `~/.multiformat_validator/plugins/`
- **Hash Verification**: SHA-256 checksums detect plugin tampering
- **Confirmation Required**: Users must confirm before loading plugins
- **Registry Tracking**: Plugin metadata stored with hash for integrity checks

#### 3. File Path Security

- **Path Normalization**: All paths resolved with `os.path.realpath()` and `os.path.abspath()`
- **Traversal Protection**: `../` and symlink attacks are neutralized
- **Protected Paths**: System directories (`C:\Windows`, `/etc`, etc.) are blocked from scanning

#### 4. Thread Safety

- **File Locks**: History and configuration files use `threading.Lock`
- **Race Condition Prevention**: Parallel scanning safely handles shared resources

#### 5. Error Handling

- **Graceful Degradation**: `PermissionError`, `FileNotFoundError`, `OSError` handled properly
- **No Crash on Bad Files**: Empty or corrupted files return error messages instead of crashing
- **Encoding Fallback**: Multiple encoding attempts with latin-1 final fallback

#### 6. XML Security (XXE Protection)

- **SAX Parser**: Uses `xml.sax` instead of `xml.etree.ElementTree`
- **External Entities Disabled**: `feature_external_ges=False`, `feature_external_pes=False`
- **No XML Bomb Vulnerability**: Prevents Billion Laughs attack

#### 7. ReDoS Protection

- **Line Length Limit**: Regex matching limited to 1000 characters per line
- **Catastrophic Backtracking Prevention**: Limits input to prevent CPU exhaustion

#### 8. Auto-fix Safety

- **Backup Before Fix**: Creates `.bak` file before modifying original
- **Diff Preview**: Shows colorized diff before user confirms changes
- **Config Corruption Recovery**: Auto-resets corrupted config files

#### 9. Path Security

- **Exclude Pattern Matching**: Uses path segments, not substrings
- **Symlink Loop Detection**: Tracks visited real paths to prevent infinite recursion

### Security Best Practices

1. Only validate files you trust
2. Only load plugins from trusted sources
3. Review custom validator code before enabling
4. Use in isolated environments (e.g., virtual environment)
5. Keep the tool updated to the latest version

### Reporting Vulnerabilities

If you find a security vulnerability, please open a public GitHub issue or contact the author through GitHub private messaging.

When reporting, please include:
- Vulnerability description
- Steps to reproduce
- Potential impact

We will fix confirmed vulnerabilities as soon as possible.

### Dependencies

| Package | Purpose | License |
|---------|---------|---------|
| colorama | Terminal colors | BSD-3-Clause |
| pyyaml | YAML support (optional) | MIT |

### Contact

For security issues, please contact Kerby Chow through the GitHub repository.

---

## 繁體中文

### 本專案的安全特性

MultiFormat Validator CLI 包含以下安全措施：

#### 1. 自訂驗證器（exec() 沙箱化）

- **靜態分析**：所有自訂驗證器程式碼在執行前會經過 `ast.parse()` 解析
- **阻止操作**：禁止 `import`、`__import__`、`exec`、`eval`、`open`、`compile`
- **受限內建函式**：僅允許安全的函式（print、len、range、str、int 等）
- **模組保護**：阻止存取 `os`、`sys`、`shutil`、`subprocess`

#### 2. 插件系統（安全載入）

- **路徑驗證**：插件必須位於 `~/.multiformat_validator/plugins/` 目錄
- **哈希校驗**：SHA-256 校驗和偵測插件是否被竄改
- **確認機制**：載入插件前需要使用者確認
- **登錄追蹤**：插件中繼資料含哈希值以確保完整性

#### 3. 檔案路徑安全

- **路徑正規化**：所有路徑經過 `os.path.realpath()` 和 `os.path.abspath()` 解析
- **遍歷防護**：`../` 和符號連結攻擊已被中和
- **保護路徑**：系統目錄（`C:\Windows`、`/etc` 等）禁止掃描

#### 4. 執行緒安全

- **檔案鎖**：歷史和設定檔使用 `threading.Lock`
- **競態條件防護**：平行掃描安全處理共享資源

#### 5. 錯誤處理

- **優雅降級**：妥善處理 `PermissionError`、`FileNotFoundError`、`OSError`
- **損壞檔案不崩潰**：空白或損壞的檔案回傳錯誤訊息而非崩潰
- **編碼降級**：多次嘗試不同編碼，最終使用 latin-1 作為備案

#### 6. XML 安全（XXE 防護）

- **SAX 解析器**：使用 `xml.sax` 而非 `xml.etree.ElementTree`
- **禁用外部實體**：`feature_external_ges=False`、`feature_external_pes=False`
- **無 XML 炸彈漏洞**：防止 Billion Laughs 攻擊

#### 7. ReDoS 防護

- **行長度限制**：正則表達式匹配限制每行 1000 字元
- **防止災難性回溯**：限制輸入以防止 CPU 耗盡

#### 8. 自動修復安全

- **修復前備份**：修改原始檔案前建立 `.bak` 備份
- **差異預覽**：使用者確認前顯示色彩化差異
- **設定損壞恢復**：自動重設損壞的設定檔

#### 9. 路徑安全

- **排除模式匹配**：使用路徑段而非子字串
- **符號連結迴圈偵測**：追蹤已訪問的真實路徑以防止無限遞迴

### 安全使用建議

1. 只驗證您信任的檔案
2. 只從可信來源載入插件
3. 啟用自訂驗證器前先檢查程式碼
4. 在隔離環境（如虛擬環境）中使用
5. 保持工具更新至最新版本

### 回報安全漏洞

如果您發現安全漏洞，請不要公開在 GitHub Issues 中。請透過 GitHub 私訊聯繫作者。

回報時請包含：
- 漏洞描述
- 重現步驟
- 影響範圍

我們會在確認後盡快修復。

### 依賴套件

| 套件 | 用途 | 授權 |
|------|------|------|
| colorama | 終端機色彩 | BSD-3-Clause |
| pyyaml | YAML 支援（可選） | MIT |

### 聯絡方式

如有安全相關問題，請透過 GitHub 倉庫私訊或填寫 Google 表單：https://forms.gle/1ZdqCtdPerYrzuzM7 聯繫作者 Kerby Chow。
