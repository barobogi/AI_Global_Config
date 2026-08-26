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
        // 로컬 개발 시 10.0.2.2 (Android 에뮬레이터) 또는 로컬 PC IP
        private const val BASE_URL = "http://10.0.2.2:8000/"

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
