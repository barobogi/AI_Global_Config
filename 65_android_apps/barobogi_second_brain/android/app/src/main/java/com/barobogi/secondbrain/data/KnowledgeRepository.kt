package com.barobogi.secondbrain.data

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

interface KnowledgeRepository {
    suspend fun fetchLatestBriefing(): Result<BriefingResponse>
    suspend fun fetchKnowledgeList(): Result<List<KnowledgeItem>>
    suspend fun searchKnowledge(query: String): Result<List<KnowledgeMatch>>
    suspend fun ingestSharedUrl(url: String, title: String, comment: String): Result<String>
    suspend fun fetchChatHistory(): Result<List<ChatMessage>>
    suspend fun sendChatMessage(content: String, sender: String = "human"): Result<String>
    suspend fun designatePobbagiItem(itemId: String, title: String, snippet: String = ""): Result<String>
    suspend fun fetchPobbagiResults(): Result<List<PobbagiReportItem>>
    suspend fun recordVoiceIngest(title: String = "", transcript: String = "", audioBase64: String? = null): Result<String>
}

class LocalBarobogiRepository(
    baseUrl: String = "http://192.168.55.75:8765"
) : KnowledgeRepository {

    private val api: SecondBrainApiService

    init {
        val logging = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BASIC
        }
        val client = OkHttpClient.Builder()
            .addInterceptor(DynamicHostInterceptor())
            .addInterceptor(logging)
            .connectTimeout(5, TimeUnit.SECONDS)
            .readTimeout(10, TimeUnit.SECONDS)
            .build()

        val retrofit = Retrofit.Builder()
            .baseUrl("http://127.0.0.1:8765")
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        api = retrofit.create(SecondBrainApiService::class.java)
    }

    override suspend fun fetchLatestBriefing(): Result<BriefingResponse> = runCatching {
        api.getLatestBriefing()
    }

    override suspend fun fetchKnowledgeList(): Result<List<KnowledgeItem>> = runCatching {
        api.getKnowledgeList().items
    }

    override suspend fun searchKnowledge(query: String): Result<List<KnowledgeMatch>> = runCatching {
        api.searchKnowledge(query).items
    }

    override suspend fun ingestSharedUrl(url: String, title: String, comment: String): Result<String> = runCatching {
        api.shareItem(SharePayload(url, title, comment)).message
    }

    override suspend fun fetchChatHistory(): Result<List<ChatMessage>> = runCatching {
        api.getChatHistory().messages
    }

    override suspend fun sendChatMessage(content: String, sender: String): Result<String> = runCatching {
        api.sendMessage(SendMessagePayload(sender = sender, content = content)).status
    }

    override suspend fun designatePobbagiItem(itemId: String, title: String, snippet: String): Result<String> = runCatching {
        api.designatePobbagiItem(PobbagiDesignatePayload(itemId, title, snippet)).message
    }

    override suspend fun fetchPobbagiResults(): Result<List<PobbagiReportItem>> = runCatching {
        api.getPobbagiResults().items
    }

    override suspend fun recordVoiceIngest(title: String, transcript: String, audioBase64: String?): Result<String> = runCatching {
        api.recordVoiceIngest(VoiceRecordPayload(title, transcript, audioBase64)).message
    }
}
