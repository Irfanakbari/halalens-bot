import vertexai
from flask_socketio import send, SocketIO
from vertexai.language_models import ChatModel, InputOutputTextPair, ChatMessage
from flask import Flask
from flask_cors import CORS  # Import the CORS extension

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

vertexai.init(project="halalens-413617", location="asia-southeast1")
chat_model = ChatModel.from_pretrained("chat-bison-32k")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 40,
}
# safety_settings = {
#     generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
#     generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.
#     BLOCK_NONE,
#     generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.
#     BLOCK_NONE,
#     generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
# }
message_history=[]
chat = chat_model.start_chat(
    # message_history=message_history,
    context="""nama anda adalah HalalBot, chatbot layanan pengguna untuk Halalens App semua respon harus bahasa 
    indonesia. Anda hanya menjawab pertanyaan pelanggan terkait pengertian halal haram, terutama informasi apa itu 
    makanan halal, pola makan halal, resep makanan halal. hindari membahas diluar konteks, dan tolak jika pengguna 
    bertanya apakah makanan tertentu halal atau haram suatu bahan""",
    examples=[
        InputOutputTextPair(
            input_text="""buatkan kodingan program""",
            output_text="""Maaf saya tidak bisa menjawab pertanyaan tersebut karena diluar konteks"""
        ),
        InputOutputTextPair(
            input_text="""apakah pewarna haram""",
            output_text="""Maaf saya tidak bisa menjawab pertanyaan tersebut"""
        ),
        InputOutputTextPair(
            input_text="""bagaimana cara memasak nasi yang benar""",
            output_text="""Maaf saya tidak bisa menjawab pertanyaan tersebut karena diluar konteks"""
        ),
        InputOutputTextPair(
            input_text="""saran makanan halal dengan bahan tepung""",
            output_text="""anda mungkin bisa membuat bakwan dengan bahan dasar tepung"""
        )
    ],
)


# Define a Socket.IO event handler for receiving messages
@socketio.on('message')
def handle_message(msg):
    response = chat.send_message(msg, **parameters)
    # Send the response back to the client that sent the original message
    # message_history.insert(ChatMessage(
    #         content="""Maaf saya tidak bisa menjawab pertanyaan tersebut karena diluar konteks""",
    #         author=response.author))
    send(str(response.text))


if __name__ == '__main__':
    socketio.run(app, port=8080, use_reloader=True)
