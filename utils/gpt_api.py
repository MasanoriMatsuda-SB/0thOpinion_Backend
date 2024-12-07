import openai
from config import Config

def get_gpt_response(prompt):
    openai.api_key = Config.OPENAI_API_KEY

    try:
        response = openai.chat.completions.create(
            model='gpt-4o',  # 使用するモデル名
            messages=[
                {'role': 'system', 'content': 'あなたは優秀な獣医師です。ペットの情報とユーザーからの質問に基づいて適切なアドバイスを提供してください。'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=300
        )

        # レスポンスからAIの応答を取得
        ai_reply = response.choices[0].message.content.strip()
        return ai_reply
    except openai.error.OpenAIError as e:
        # エラーハンドリング
        print(f"OpenAI API エラー: {e}")
        return "AI応答を取得中にエラーが発生しました。"
