import openai
from config import Config

def get_gpt_response(prompt):
    openai.api_key = Config.OPENAI_API_KEY

    try:
        response = openai.chat.completions.create(
            model='gpt-4o',  # 使用するモデル名
            messages=[
                {'role': 'system', 'content': 'あなたは優秀な獣医師です。ペット(犬)の情報とユーザーからの質問に基づいて適切なアドバイスを提供してください。冒頭に飼い主への優しいメッセージ、1.考えられる要因（可能性が高い順に3つ）、2.病院に行く際に記録すべき内容を含める。600字以内。回答内容は、高校生の読解力で理解できるレベルを基準に作成する。以下の回答をMarkdownや装飾を使用せずにプレーンテキストで返してください。'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=600
        )

        # レスポンスからAIの応答を取得
        ai_reply = response.choices[0].message.content.strip()
        return ai_reply
    except openai.error.OpenAIError as e:
        # エラーハンドリング
        print(f"OpenAI API エラー: {e}")
        return "AI応答を取得中にエラーが発生しました。"
