# OPTIC-NERVE-MCP Walkthrough

[English](#english) | [日本語](#japanese)

<a name="english"></a>
## English Version

### Overview
This project implements a biological-grade AI Vision Interface using the **Model Context Protocol (MCP)**. It serves as an "Eye" for an LLM, capturing webcam frames and serving them via MCP tools.

### Features (v2 Evolution)
- **AdaptiveRetina v2**:
    - **Sensory Qualia**: Calculates `brightness` and `motion` delta for every frame.
    - **Metabolic Auto-Regulation**: Automatically slows down to 1 frame/min if ignored for 5 minutes. Wakes up instantly on access.
    - **Multi-Camera Failover**: Automatically scans for other cameras if the primary one fails.
- **Latest Frame Drop**: Always serves the freshest photon.
- **MCP Tools**:
    - `read_eye()`: Get visual field + sensory metadata.
    - `configure_eye(interval)`: Adjust the base heartbeat.

### Usage

#### 1. Start the Server
```bash
cd /Users/kuyu/Library/CloudStorage/GoogleDrive-annpannmannnouta@gmail.com/マイドライブ/プログラミング/optic-nerve-mcp
python3 server.py
```

#### 2. Connect via MCP
Configure your MCP client (e.g., Claude Desktop, Antigravity) to use the stdio transport with the command above.

#### 3. Tools
- **`read_eye`**: Call this to see.
- **`configure_eye`**: Call this to change speed.
    - `0.0`: Max speed (Real-time)
    - `5.0`: Low metabolism (Default)
    - `300.0`: Deep hibernation (1 frame/5min)

### Verification
A test script `test_retina.py` is included to verify the camera logic without running the full MCP server.
```bash
python3 test_retina.py
```
Expected output:
```
Initializing Retina...
Starting Retina (Interval: 1.0s)...
...
Retina connected.
Reading Eye (Attempt 1)...
Status: SIGHT
Image captured! Length: 706704 chars
Stopping Retina...
Test Complete.
```

#### Troubleshooting
- **macOS Camera Permission**: If you see `OpenCV: not authorized to capture video`, you must grant camera access to your terminal (iTerm, VSCode, etc.) in `System Settings > Privacy & Security > Camera`.

### Setup on New Device

To run this project on another machine:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/annpannmannnouta-afk/OPTIC-NERVE-MCP-Walkthrough.git
    cd OPTIC-NERVE-MCP-Walkthrough
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the server**:
    ```bash
    python3 server.py
    ```

### How to Update
To get the latest version (e.g., v2 upgrade) on an existing machine:
```bash
git pull
```
*This command downloads the latest changes from GitHub and merges them into your local folder.*

---

<a name="japanese"></a>
## 日本語版 (Japanese Version)

### 概要
このプロジェクトは、**Model Context Protocol (MCP)** を使用した、生物学的グレードのAI視覚インターフェースを実装します。これはLLMの「目」として機能し、ウェブカメラの映像をキャプチャしてMCPツール経由で提供します。

### 機能 (v2 進化版)
- **AdaptiveRetina v2 (適応型網膜)**:
    - **感覚クオリア**: フレームごとに「明るさ」と「動き」の変化量を計算します。
    - **代謝の自動調節**: 5分間放置されると自動的に1フレーム/分の速度に落とし、アクセスされると即座に覚醒します。
    - **多眼フェイルオーバー**: メインカメラが故障した場合、自動的に他のカメラをスキャンして接続します。
- **最新フレームドロップ**: 常に「最も新鮮な光子（最新フレーム）」のみを提供し、古いデータは破棄します。
- **MCPツール**:
    - `read_eye()`: 視界と感覚メタデータを取得します。
    - `configure_eye(interval)`: 基本の心拍数（撮影間隔）を調整します。

### 使用方法

#### 1. サーバーの起動
```bash
cd /Users/kuyu/Library/CloudStorage/GoogleDrive-annpannmannnouta@gmail.com/マイドライブ/プログラミング/optic-nerve-mcp
python3 server.py
```

#### 2. MCP経由での接続
お使いのMCPクライアント（Claude Desktop, Antigravityなど）を設定し、上記のコマンドでstdio転送を使用するようにしてください。

#### 3. ツール
- **`read_eye`**: 「見る」ために呼び出します。
- **`configure_eye`**: 速度を変更するために呼び出します。
    - `0.0`: 最高速度（リアルタイム）
    - `5.0`: 低代謝モード（デフォルト）
    - `300.0`: 深い冬眠（5分に1フレーム）

### 検証
MCPサーバー全体を起動せずにカメラロジックを検証するためのテストスクリプト `test_retina.py` が含まれています。
```bash
python3 test_retina.py
```
期待される出力:
```
Initializing Retina...
Starting Retina (Interval: 1.0s)...
...
Retina connected.
Reading Eye (Attempt 1)...
Status: SIGHT
Image captured! Length: 706704 chars
Stopping Retina...
Test Complete.
```

#### トラブルシューティング
- **macOSのカメラ権限**: もし `OpenCV: not authorized to capture video` というエラーが表示された場合、`システム設定 > プライバシーとセキュリティ > カメラ` で、使用しているターミナル（iTerm, VSCodeなど）にカメラへのアクセス権限を許可する必要があります。

### 新しいデバイスでのセットアップ

別のマシンでこのプロジェクトを実行するには:

1.  **リポジトリをクローンする**:
    ```bash
    git clone https://github.com/annpannmannnouta-afk/OPTIC-NERVE-MCP-Walkthrough.git
    cd OPTIC-NERVE-MCP-Walkthrough
    ```

2.  **依存関係をインストールする**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **サーバーを起動する**:
    ```bash
    python3 server.py
    ```

### 更新方法
既存のマシンで最新バージョン（v2アップグレードなど）を取得するには:
```bash
git pull
```
*このコマンドは、GitHubから最新の変更をダウンロードし、ローカルフォルダに統合します。*
