package com.barobogi.secondbrain.data

import android.content.Context
import android.content.SharedPreferences
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.*
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull
import java.io.IOException
import java.util.concurrent.TimeUnit

object ServerConfig {
    private const val PREFS_NAME = "second_brain_server_prefs"
    private const val KEY_INTERNAL_URL = "key_internal_url"
    private const val KEY_EXTERNAL_URL = "key_external_url"
    private const val KEY_SELECTED_MODE = "key_selected_mode" // "AUTO", "INTERNAL", "EXTERNAL"

    const val DEFAULT_INTERNAL_URL = "http://192.168.55.75:8765"
    const val DEFAULT_EXTERNAL_URL = "https://arrives-engine-structures-depends.trycloudflare.com"

    @Volatile
    var activeBaseUrl: String = DEFAULT_EXTERNAL_URL
        private set

    @Volatile
    var isExternalMode: Boolean = true
        private set

    fun init(context: Context) {
        val prefs = getPrefs(context)
        val mode = prefs.getString(KEY_SELECTED_MODE, "AUTO") ?: "AUTO"
        val internalUrl = prefs.getString(KEY_INTERNAL_URL, DEFAULT_INTERNAL_URL) ?: DEFAULT_INTERNAL_URL
        var externalUrl = prefs.getString(KEY_EXTERNAL_URL, DEFAULT_EXTERNAL_URL) ?: DEFAULT_EXTERNAL_URL

        // 구버전 터널 주소가 SharedPreferences에 남아있을 경우 최신 DEFAULT_EXTERNAL_URL로 강제 보정
        if (!externalUrl.startsWith("http") || externalUrl.contains("trycloudflare.com") && externalUrl != DEFAULT_EXTERNAL_URL) {
            externalUrl = DEFAULT_EXTERNAL_URL
            saveUrls(context, internalUrl, DEFAULT_EXTERNAL_URL)
        }

        activeBaseUrl = when (mode) {
            "INTERNAL" -> {
                isExternalMode = false
                internalUrl
            }
            "EXTERNAL" -> {
                isExternalMode = true
                externalUrl
            }
            else -> externalUrl
        }
    }

    private fun getPrefs(context: Context): SharedPreferences =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun getInternalUrl(context: Context): String =
        getPrefs(context).getString(KEY_INTERNAL_URL, DEFAULT_INTERNAL_URL) ?: DEFAULT_INTERNAL_URL

    fun getExternalUrl(context: Context): String =
        getPrefs(context).getString(KEY_EXTERNAL_URL, DEFAULT_EXTERNAL_URL) ?: DEFAULT_EXTERNAL_URL

    fun saveUrls(context: Context, internalUrl: String, externalUrl: String) {
        getPrefs(context).edit()
            .putString(KEY_INTERNAL_URL, internalUrl.trimEnd('/'))
            .putString(KEY_EXTERNAL_URL, externalUrl.trimEnd('/'))
            .apply()
    }

    /**
     * 800ms 내에 내부 Wi-Fi 연결 여부를 핑으로 확인하고,
     * 연결 불가 시(방화벽/모바일 데이터 상태) 자동으로 외부 터널 주소로 전환하는 Zero-Config 스위치
     */
    suspend fun autoDetectAndSwitch(context: Context): Boolean = withContext(Dispatchers.IO) {
        val internal = getInternalUrl(context)
        var external = getExternalUrl(context)

        val pingClient = OkHttpClient.Builder()
            .connectTimeout(800, TimeUnit.MILLISECONDS)
            .readTimeout(800, TimeUnit.MILLISECONDS)
            .build()

        // 1. 내부 IP 핑 테스트 (/api/v1/health)
        val isInternalReachable = try {
            val req = Request.Builder().url("$internal/api/v1/health").build()
            val resp = pingClient.newCall(req).execute()
            resp.isSuccessful
        } catch (e: Exception) {
            false
        }

        if (isInternalReachable) {
            activeBaseUrl = internal
            isExternalMode = false
        } else {
            // 2. 외부 터널 주소 핑 테스트 (/api/v1/health)
            val isExternalReachable = try {
                val req = Request.Builder().url("$external/api/v1/health").build()
                val resp = pingClient.newCall(req).execute()
                resp.isSuccessful
            } catch (e: Exception) {
                false
            }

            if (isExternalReachable) {
                activeBaseUrl = external
                isExternalMode = true
            } else {
                // 3. 저장된 외부 주소가 구버전일 경우 DEFAULT_EXTERNAL_URL 자동 치환 및 복구
                val isDefaultReachable = try {
                    val req = Request.Builder().url("$DEFAULT_EXTERNAL_URL/api/v1/health").build()
                    val resp = pingClient.newCall(req).execute()
                    resp.isSuccessful
                } catch (e: Exception) {
                    false
                }

                if (isDefaultReachable || external != DEFAULT_EXTERNAL_URL) {
                    external = DEFAULT_EXTERNAL_URL
                    saveUrls(context, internal, DEFAULT_EXTERNAL_URL)
                }
                activeBaseUrl = external
                isExternalMode = true
            }
        }
        android.util.Log.d("ServerConfig", "autoDetectAndSwitch finished: activeBaseUrl=$activeBaseUrl, isExternalMode=$isExternalMode")

        isExternalMode
    }
}

/**
 * 런타임에 activeBaseUrl에 맞춰 요청 Host/Scheme/Port를 실시간 치환하는 OkHttp Interceptor
 */
class DynamicHostInterceptor : Interceptor {
    @Throws(IOException::class)
    override fun intercept(chain: Interceptor.Chain): Response {
        var request = chain.request()
        val currentTarget = ServerConfig.activeBaseUrl.toHttpUrlOrNull()

        if (currentTarget != null) {
            val newUrl = request.url.newBuilder()
                .scheme(currentTarget.scheme)
                .host(currentTarget.host)
                .port(currentTarget.port)
                .build()
            request = request.newBuilder().url(newUrl).build()
        }

        return chain.proceed(request)
    }
}
