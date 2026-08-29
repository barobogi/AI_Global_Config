package com.barobogi.todaywhattodo.data.api

import com.barobogi.todaywhattodo.data.model.RecommendRequest
import com.barobogi.todaywhattodo.data.model.RecommendResponse
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import java.util.concurrent.TimeUnit

interface TodayApiService {
    @POST("/api/recommend")
    suspend fun getRecommendations(@Body request: RecommendRequest): RecommendResponse

    @GET("/api/health")
    suspend fun checkHealth(): Map<String, Any>

    companion object {
        // Render.com 상시 클라우드 배포 서버 주소
        private const val BASE_URL = "https://today-what-to-do-api.onrender.com/"

        fun create(): TodayApiService {
            val logging = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }
            val client = OkHttpClient.Builder()
                .addInterceptor(logging)
                .connectTimeout(10, TimeUnit.SECONDS)
                .readTimeout(15, TimeUnit.SECONDS)
                .build()

            return Retrofit.Builder()
                .baseUrl(BASE_URL)
                .client(client)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(TodayApiService::class.java)
        }
    }
}
