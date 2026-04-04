import asyncio
import sys
from typing import Optional

from browser_use import Agent, Browser
from browser_use.llm.ollama.chat import ChatOllama

# ==========================================
# 設定エリア
# ==========================================
# 使用するOllamaのモデル名
MODEL_NAME = "llama3.2:1b"

# ==========================================
# メイン処理
# ==========================================
async def main():
    """
    Gemma 4を使用してブラウザ操作を行うメイン関数。
    """
    print(f"--- Gemma 4 ブラウザエージェント起動 ---")
    print(f"使用モデル: {MODEL_NAME}")
    
    # ユーザーからの入力を取得（コマンドライン引数がない場合はデフォルト）
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        # デフォルトのタスク例（Google検索ベースで軽量化）
        task = "Google検索で青森市周辺の評価の高い居酒屋を3軒探して、それぞれの店名と特徴を簡潔に教えてください。"

    print(f"実行タスク: {task}")
    print("-" * 40)

    # Ollamaモデルの初期化
    llm = ChatOllama(
        model=MODEL_NAME,
        timeout=300.0,
        ollama_options={
            "num_ctx": 4096, # 記憶容量を最小限にして読み込み（プリフィル）を爆速化
            "temperature": 0.0,
            "num_predict": 256, # 回答を短くして生成速度を向上
        }
    )

    # ブラウザの設定
    browser = Browser(
        headless=False,
        disable_security=True,
        args=["--disable-gpu", "--disable-software-rasterizer"]
    )

    # エージェントの作成
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        llm_timeout=600,
        step_timeout=900,
        use_vision=True,
        # 画像サイズをさらに縮小
        llm_screenshot_size=(300, 300),
        # 属性を極限まで絞り込み、AIに送るテキスト量を最小にする
        include_attributes=['title', 'aria-label'],
        extend_system_message="あなたは高速な操作エージェントです。余計なことは考えず、検索窓を見つけてキーワードを入力し、結果を3つ選んでください。簡潔に行動してください。",
    )

    try:
        # 実行開始
        result = await agent.run()
        
        print("\n" + "=" * 40)
        print("【実行完了】")
        print(result)
        print("=" * 40)
        
    except Exception as e:
        print(f"\n[エラーが発生しました] {e}")
        print("Ollamaが起動しているか、モデル 'gemma4:e4b' がダウンロード済みか確認してください。")
    finally:
        if hasattr(browser, 'close'):
            await browser.close()
        elif hasattr(browser, 'stop'):
            await browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
