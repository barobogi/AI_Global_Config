package com.barobogi.secondbrain

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.media.MediaRecorder
import android.os.Build
import android.os.Bundle
import android.util.Base64
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlinx.coroutines.delay
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.ImeAction
import com.barobogi.secondbrain.data.BriefingResponse
import com.barobogi.secondbrain.data.KnowledgeMatch
import com.barobogi.secondbrain.data.LocalBarobogiRepository
import com.barobogi.secondbrain.data.ServerConfig
import kotlinx.coroutines.launch
import androidx.lifecycle.lifecycleScope

class MainActivity : ComponentActivity() {

    private val repository = LocalBarobogiRepository()
    private var mediaPlayer: MediaPlayer? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        ServerConfig.init(this)
        // 앱 시작 시 내부·외부 URL을 자동으로 탐지하고 activeBaseUrl 를 설정합니다.
        lifecycleScope.launch {
            // 탐지 결과에 따라 UI 상태가 자동 업데이트됩니다.
            ServerConfig.autoDetectAndSwitch(this@MainActivity)
        }
        setContent {
            SecondBrainApp(
                repository = repository,
                onPlayAudio = { url -> playAudio(url) },
                onStopAudio = { stopAudio() }
            )
        }
    }

    private fun playAudio(url: String) {
        stopAudio()
        try {
            mediaPlayer = MediaPlayer().apply {
                setAudioAttributes(
                    AudioAttributes.Builder()
                        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                        .setUsage(AudioAttributes.USAGE_MEDIA)
                        .build()
                )
                val fullUrl = if (url.startsWith("http")) url else "${ServerConfig.activeBaseUrl}$url"
                setDataSource(fullUrl)
                prepareAsync()
                setOnPreparedListener { start() }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun stopAudio() {
        mediaPlayer?.release()
        mediaPlayer = null
    }

    override fun onDestroy() {
        super.onDestroy()
        stopAudio()
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SecondBrainApp(
    repository: LocalBarobogiRepository,
    onPlayAudio: (String) -> Unit,
    onStopAudio: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    var selectedTab by remember { mutableStateOf(0) }
    var showSettingsDialog by remember { mutableStateOf(false) }
    var showVoiceRecordDialog by remember { mutableStateOf(false) }
    var isExternal by remember { mutableStateOf(ServerConfig.isExternalMode) }
    var isCheckingNetwork by remember { mutableStateOf(false) }

    var latestBriefing by remember { mutableStateOf<BriefingResponse?>(null) }
    var searchQuery by remember { mutableStateOf("") }
    var searchResults by remember { mutableStateOf<List<KnowledgeMatch>>(emptyList()) }
    var knowledgeList by remember { mutableStateOf<List<com.barobogi.secondbrain.data.KnowledgeItem>>(emptyList()) }
    var pobbagiReports by remember { mutableStateOf<List<com.barobogi.secondbrain.data.PobbagiReportItem>>(emptyList()) }
    var designatedItemIds by remember { mutableStateOf<Set<String>>(emptySet()) }
    var playingAudioUrl by remember { mutableStateOf<String?>(null) }
    var playingItemId by remember { mutableStateOf<String?>(null) }
    var selectedKnowledgeDetailItem by remember { mutableStateOf<com.barobogi.secondbrain.data.KnowledgeItem?>(null) }

    // 3AI 채팅 관련 상태
    var chatMessages by remember { mutableStateOf<List<com.barobogi.secondbrain.data.ChatMessage>>(emptyList()) }
    var inputMessage by remember { mutableStateOf("") }
    var isSending by remember { mutableStateOf(false) }

    val listState = androidx.compose.foundation.lazy.rememberLazyListState()

    // 앱 실행 시 자동 네트워크 감지 및 스위칭 (Wi-Fi vs LTE/모바일 데이터)
    LaunchedEffect(Unit) {
        isCheckingNetwork = true
        isExternal = ServerConfig.autoDetectAndSwitch(context)
        isCheckingNetwork = false

        repository.fetchLatestBriefing().onSuccess { latestBriefing = it }
        repository.fetchKnowledgeList().onSuccess { knowledgeList = it }
        repository.fetchPobbagiResults().onSuccess { pobbagiReports = it }
        repository.fetchChatHistory().onSuccess { 
            chatMessages = it
            if (it.isNotEmpty()) {
                listState.scrollToItem(it.size - 1)
            }
        }

        // 실시간 채팅 2초 주기 자동 갱신 (Web UI와 동일 동기화)
        while (true) {
            kotlinx.coroutines.delay(2000)
            repository.fetchChatHistory().onSuccess { newMsgs ->
                if (newMsgs.size != chatMessages.size || (newMsgs.isNotEmpty() && chatMessages.isNotEmpty() && newMsgs.last().msgId != chatMessages.last().msgId)) {
                    val wasAtBottom = listState.firstVisibleItemIndex + listState.layoutInfo.visibleItemsInfo.size >= chatMessages.size - 1
                    chatMessages = newMsgs
                    if (wasAtBottom && newMsgs.isNotEmpty()) {
                        listState.animateScrollToItem(newMsgs.size - 1)
                    }
                }
            }
        }
    }

    LaunchedEffect(selectedTab) {
        if (selectedTab == 0) {
            repository.fetchLatestBriefing().onSuccess { latestBriefing = it }
        } else if (selectedTab == 3) {
            repository.fetchKnowledgeList().onSuccess { knowledgeList = it }
        } else if (selectedTab == 4) {
            repository.fetchPobbagiResults().onSuccess { pobbagiReports = it }
        }
    }


    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("바로보기 세컨드 브레인", fontWeight = FontWeight.Bold, fontSize = 17.sp)
                        Spacer(modifier = Modifier.width(8.dp))
                        // 스마트 네트워크 연결 상태 배지
                        val badgeText = if (isCheckingNetwork) "연결 감지 중..." else if (isExternal) "🌐 모바일LTE" else "🟢 집Wi-Fi"
                        val badgeColor = if (isExternal) Color(0xFF38BDF8) else Color(0xFF4ADE80)
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = badgeColor.copy(alpha = 0.2f),
                            modifier = Modifier.padding(horizontal = 4.dp)
                        ) {
                            Text(
                                badgeText,
                                color = badgeColor,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.SemiBold,
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }
                },
                actions = {
                    IconButton(onClick = { showVoiceRecordDialog = true }) {
                        Icon(Icons.Default.Mic, contentDescription = "1-Tap PLAUD 음성 녹음", tint = Color(0xFFF43F5E))
                    }
                    IconButton(onClick = { showSettingsDialog = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "서버 설정", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color(0xFF0F172A),
                    titleContentColor = Color.White
                )
            )
        },
        bottomBar = {
            NavigationBar(containerColor = Color(0xFF0F172A)) {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    icon = { Icon(Icons.Default.Radio, contentDescription = "라디오") },
                    label = { Text("오디오 브리핑") }
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    icon = { Icon(Icons.Default.Chat, contentDescription = "3AI 채팅") },
                    label = { Text("3AI 채팅") }
                )
                NavigationBarItem(
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 },
                    icon = { Icon(Icons.Default.Search, contentDescription = "지식 검색") },
                    label = { Text("지식 검색") }
                )
                NavigationBarItem(
                    selected = selectedTab == 3,
                    onClick = { selectedTab = 3 },
                    icon = { Icon(Icons.Default.MenuBook, contentDescription = "지식 DB") },
                    label = { Text("지식 DB") }
                )
                NavigationBarItem(
                    selected = selectedTab == 4,
                    onClick = { selectedTab = 4 },
                    icon = { Icon(Icons.Default.Build, contentDescription = "🔥 뽀개기") },
                    label = { Text("🔥 뽀개기") }
                )
            }
        },
        containerColor = Color(0xFF0B0F19)
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            when (selectedTab) {
                0 -> {
                    // [탭 1] 아침 오디오 브리핑 카드
                    latestBriefing?.let { briefing ->
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)),
                            shape = RoundedCornerShape(16.dp)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = "${briefing.date} (${briefing.day})",
                                        color = Color(0xFF38BDF8),
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 14.sp
                                    )
                                    Text(
                                        text = "3AI 모닝 테크",
                                        color = Color.Gray,
                                        fontSize = 12.sp
                                    )
                                }

                                Spacer(modifier = Modifier.height(8.dp))
                                Text(
                                    text = briefing.topic,
                                    color = Color.White,
                                    fontWeight = FontWeight.ExtraBold,
                                    fontSize = 18.sp
                                )

                                Spacer(modifier = Modifier.height(12.dp))
                                val summaryText = briefing.dialogue.joinToString("\n") { "${it.speaker}: ${it.text}" }
                                Text(
                                    text = summaryText,
                                    color = Color(0xFFCBD5E1),
                                    fontSize = 14.sp,
                                    lineHeight = 20.sp
                                )

                                Spacer(modifier = Modifier.height(16.dp))

                                val currentAudioUrl = briefing.audioUrl
                                val isThisPlaying = playingAudioUrl == currentAudioUrl && playingItemId == "TAB_0_BRIEFING"
                                Button(
                                    onClick = {
                                        if (isThisPlaying) {
                                            onStopAudio()
                                            playingAudioUrl = null
                                            playingItemId = null
                                        } else {
                                            onPlayAudio(currentAudioUrl)
                                            playingAudioUrl = currentAudioUrl
                                            playingItemId = "TAB_0_BRIEFING"
                                        }
                                    },
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = if (isThisPlaying) Color(0xFFEF4444) else Color(0xFF0284C7)
                                    ),
                                    modifier = Modifier.fillMaxWidth(),
                                    shape = RoundedCornerShape(10.dp)
                                ) {
                                    Icon(
                                        imageVector = if (isThisPlaying) Icons.Default.Stop else Icons.Default.PlayArrow,
                                        contentDescription = if (isThisPlaying) "정지" else "재생"
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(if (isThisPlaying) "오디오 브리핑 정지" else "3AI 대화형 브리핑 듣기")
                                }
                            }
                        }
                    } ?: run {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                CircularProgressIndicator(color = Color(0xFF38BDF8))
                                Spacer(modifier = Modifier.height(12.dp))
                                Text("오늘의 오디오 브리핑을 불러오는 중...", color = Color.Gray)
                                Spacer(modifier = Modifier.height(12.dp))
                                Button(
                                    onClick = {
                                        scope.launch {
                                            repository.fetchLatestBriefing().onSuccess { latestBriefing = it }
                                        }
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0284C7))
                                ) {
                                    Icon(Icons.Default.Refresh, contentDescription = "재시도")
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text("브리핑 다시 불러오기")
                                }
                            }
                        }
                    }
                }
                1 -> {
                    // [탭 2] 3AI 실시간 채팅
                    LazyColumn(
                        state = listState,
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxWidth(),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(chatMessages) { msg ->
                            val isHuman = msg.sender.equals("human", ignoreCase = true)
                            val bubbleColor = when (msg.sender.lowercase()) {
                                "human" -> Color(0xFF0284C7)
                                "anti" -> Color(0xFF10B981)
                                "manbok" -> Color(0xFF6366F1)
                                "kony" -> Color(0xFFEC4899)
                                else -> Color(0xFF334155)
                            }
                            Column(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalAlignment = if (isHuman) Alignment.End else Alignment.Start
                            ) {
                                val timeText = msg.createdAt?.takeLast(8) ?: ""
                                Text(
                                    text = "${msg.sender} • $timeText",
                                    fontSize = 11.sp,
                                    color = Color.Gray,
                                    modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp)
                                )
                                Surface(
                                    color = bubbleColor,
                                    shape = RoundedCornerShape(12.dp)
                                ) {
                                    Text(
                                        text = msg.content,
                                        color = Color.White,
                                        fontSize = 14.sp,
                                        modifier = Modifier.padding(10.dp)
                                    )
                                }
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(8.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        OutlinedTextField(
                            value = inputMessage,
                            onValueChange = { inputMessage = it },
                            modifier = Modifier.weight(1f),
                            placeholder = { Text("3AI에게 지시 또는 질문 입력...") },
                            singleLine = true,
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedTextColor = Color.White,
                                unfocusedTextColor = Color.White,
                                focusedBorderColor = Color(0xFF38BDF8),
                                unfocusedBorderColor = Color(0xFF334155)
                            )
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        IconButton(
                            enabled = !isSending && inputMessage.isNotBlank(),
                            onClick = {
                                if (inputMessage.isNotBlank()) {
                                    isSending = true
                                    val textToSend = inputMessage
                                    inputMessage = ""
                                    scope.launch {
                                        repository.sendChatMessage(textToSend, "human").onSuccess {
                                            repository.fetchChatHistory().onSuccess { chatMessages = it }
                                        }
                                        isSending = false
                                    }
                                }
                            }
                        ) {
                            Icon(Icons.Default.Send, contentDescription = "전송", tint = Color(0xFF38BDF8))
                        }
                    }
                }
                2 -> {
                    // [탭 3] 지식 풀텍스트 검색
                    var isSearching by remember { mutableStateOf(false) }
                    var hasSearched by remember { mutableStateOf(false) }

                    val performSearch: () -> Unit = {
                        if (searchQuery.isNotBlank()) {
                            isSearching = true
                            hasSearched = true
                            scope.launch {
                                repository.searchKnowledge(searchQuery).onSuccess {
                                    searchResults = it
                                    isSearching = false
                                }.onFailure {
                                    isSearching = false
                                }
                            }
                        }
                    }

                    OutlinedTextField(
                        value = searchQuery,
                        onValueChange = { searchQuery = it },
                        modifier = Modifier.fillMaxWidth(),
                        placeholder = { Text("키워드 검색 (예: LLM, 에이전트, AI)") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                        keyboardActions = KeyboardActions(onSearch = { performSearch() }),
                        trailingIcon = {
                            IconButton(onClick = { performSearch() }) {
                                Icon(Icons.Default.Search, contentDescription = "검색", tint = Color.White)
                            }
                        },
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White,
                            focusedBorderColor = Color(0xFF38BDF8),
                            unfocusedBorderColor = Color(0xFF334155)
                        )
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    if (isSearching) {
                        Text("🔍 지식 DB 검색 중...", color = Color(0xFF38BDF8), fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                    } else if (hasSearched && searchResults.isEmpty()) {
                        Text("❌ 검색 결과가 없습니다.", color = Color(0xFFFF6B6B), fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                    } else if (hasSearched) {
                        Text("✅ 총 ${searchResults.size}건의 지식 검색 결과", color = Color(0xFF4ADE80), fontSize = 13.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(8.dp))
                    }

                    LazyColumn(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        items(searchResults) { match ->
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B))
                            ) {
                                Column(modifier = Modifier.padding(12.dp)) {
                                    Text(match.file, color = Color(0xFF38BDF8), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(match.snippet, color = Color(0xFFCBD5E1), fontSize = 13.sp)
                                }
                            }
                        }
                    }
                }
                3 -> {
                    // [탭 4] 전수 지식 DB 라이브러리 & 오디오 플레이어
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        val countDisplay = if (knowledgeList.isNotEmpty()) knowledgeList.size else 353
                        Text("📚 전수 지식 DB 라이브러리 (${countDisplay}개)", color = Color(0xFF38BDF8), fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        IconButton(onClick = {
                            scope.launch {
                                repository.fetchKnowledgeList().onSuccess { knowledgeList = it }
                            }
                        }) {
                            Icon(Icons.Default.Refresh, contentDescription = "새로고침", tint = Color(0xFF38BDF8))
                        }
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Text("총 ${if (knowledgeList.isNotEmpty()) knowledgeList.size else 353}건의 유튜브/Obsidian 노하우 중 원하시는 항목을 클릭해 청취하세요.", color = Color.Gray, fontSize = 12.sp)
                    Spacer(modifier = Modifier.height(12.dp))

                    if (knowledgeList.isEmpty()) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                CircularProgressIndicator(color = Color(0xFF38BDF8))
                                Spacer(modifier = Modifier.height(12.dp))
                                Text("지식 DB 라이브러리를 불러오는 중...", color = Color.Gray)
                                Spacer(modifier = Modifier.height(12.dp))
                                Button(
                                    onClick = {
                                        scope.launch {
                                            repository.fetchKnowledgeList().onSuccess { knowledgeList = it }
                                        }
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0284C7))
                                ) {
                                    Icon(Icons.Default.Refresh, contentDescription = "재시도")
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text("지식 DB 다시 불러오기")
                                }
                            }
                        }
                    } else {
                        LazyColumn(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            items(knowledgeList) { item ->
                                val itemAudioUrl = item.audioUrl ?: "/api/v1/knowledge/audio/${item.id}"
                                val isThisPlaying = playingAudioUrl == itemAudioUrl && playingItemId == item.id
                                Card(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable {
                                            selectedKnowledgeDetailItem = item
                                        },
                                    colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B))
                                ) {
                                    Column(modifier = Modifier.padding(12.dp)) {
                                        Row(
                                            modifier = Modifier.fillMaxWidth(),
                                            horizontalArrangement = Arrangement.SpaceBetween,
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Text(item.title, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                            Spacer(modifier = Modifier.width(8.dp))
                                            Surface(
                                                shape = RoundedCornerShape(8.dp),
                                                color = Color(0xFF0284C7).copy(alpha = 0.3f)
                                            ) {
                                                Text(
                                                    item.category ?: (item.ext?.uppercase() ?: "TXT"),
                                                    color = Color(0xFF38BDF8),
                                                    fontSize = 11.sp,
                                                    fontWeight = FontWeight.Bold,
                                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                                )
                                            }
                                        }

                                        item.keywords?.let { kwList ->
                                            if (kwList.isNotEmpty()) {
                                                Spacer(modifier = Modifier.height(4.dp))
                                                Text(
                                                    text = kwList.joinToString(" ") { "#$it" },
                                                    color = Color(0xFFA7F3D0),
                                                    fontSize = 11.sp,
                                                    fontWeight = FontWeight.Medium
                                                )
                                            }
                                        }

                                        Spacer(modifier = Modifier.height(6.dp))
                                        val bodyText = item.threeLineSummary ?: item.snippet ?: ""
                                        Text(bodyText, color = Color(0xFFCBD5E1), fontSize = 13.sp, maxLines = 3)

                                        item.deepInsights?.let { insights ->
                                            if (insights.isNotBlank()) {
                                                Spacer(modifier = Modifier.height(6.dp))
                                                Surface(
                                                    shape = RoundedCornerShape(6.dp),
                                                    color = Color(0xFF334155).copy(alpha = 0.5f)
                                                ) {
                                                    Text(
                                                        text = insights,
                                                        color = Color(0xFFFDE047),
                                                        fontSize = 12.sp,
                                                        modifier = Modifier.padding(8.dp),
                                                        maxLines = 2
                                                    )
                                                }
                                            }
                                        }

                                        Spacer(modifier = Modifier.height(10.dp))
                                        Row(
                                            modifier = Modifier.fillMaxWidth(),
                                            horizontalArrangement = Arrangement.SpaceBetween,
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Row(
                                                verticalAlignment = Alignment.CenterVertically,
                                                modifier = Modifier.clickable {
                                                    if (isThisPlaying) {
                                                        onStopAudio()
                                                        playingAudioUrl = null
                                                        playingItemId = null
                                                    } else {
                                                        onPlayAudio(itemAudioUrl)
                                                        playingAudioUrl = itemAudioUrl
                                                        playingItemId = item.id
                                                    }
                                                }
                                            ) {
                                                Icon(
                                                    imageVector = if (isThisPlaying) Icons.Default.Stop else Icons.Default.PlayArrow,
                                                    contentDescription = if (isThisPlaying) "정지" else "재생",
                                                    tint = if (isThisPlaying) Color(0xFFEF4444) else Color(0xFF4ADE80),
                                                    modifier = Modifier.size(18.dp)
                                                )
                                                Spacer(modifier = Modifier.width(4.dp))
                                                Text(
                                                    if (isThisPlaying) "1분 브리핑 정지" else "1분 브리핑 듣기",
                                                    color = if (isThisPlaying) Color(0xFFEF4444) else Color(0xFF4ADE80),
                                                    fontSize = 12.sp,
                                                    fontWeight = FontWeight.SemiBold
                                                )
                                            }

                                            val isDesignated = designatedItemIds.contains(item.id)
                                            Button(
                                                onClick = {
                                                    scope.launch {
                                                        designatedItemIds = designatedItemIds + item.id
                                                        repository.designatePobbagiItem(item.id, item.title, item.threeLineSummary ?: item.snippet ?: "")
                                                    }
                                                },
                                                colors = ButtonDefaults.buttonColors(
                                                    containerColor = if (isDesignated) Color(0xFF6366F1) else Color(0xFFE11D48)
                                                ),
                                                shape = RoundedCornerShape(6.dp),
                                                contentPadding = PaddingValues(horizontal = 8.dp, vertical = 2.dp),
                                                modifier = Modifier.height(30.dp)
                                            ) {
                                                Icon(Icons.Default.Build, contentDescription = "뽀개기", tint = Color.White, modifier = Modifier.size(13.dp))
                                                Spacer(modifier = Modifier.width(3.dp))
                                                Text(if (isDesignated) "🔨 진행중..." else "🔨 뽀개기 지정", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                            }

                                            Row(
                                                verticalAlignment = Alignment.CenterVertically,
                                                modifier = Modifier.clickable { selectedKnowledgeDetailItem = item }
                                            ) {
                                                Icon(Icons.Default.MenuBook, contentDescription = "상세보기", tint = Color(0xFF38BDF8), modifier = Modifier.size(16.dp))
                                                Spacer(modifier = Modifier.width(4.dp))
                                                Text("상세", color = Color(0xFF38BDF8), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                            }
                                        }
                                    }

                                }
                            }
                        }
                    }
                }
                4 -> {
                    // [탭 5] 3AI 뽀개기 리포트 & 실시간 사후 승인 상태
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("🔥 3AI 뽀개기 최종 리포트", color = Color(0xFFF43F5E), fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        IconButton(onClick = {
                            scope.launch {
                                repository.fetchPobbagiResults().onSuccess { pobbagiReports = it }
                            }
                        }) {
                            Icon(Icons.Default.Refresh, contentDescription = "새로고침", tint = Color(0xFFF43F5E))
                        }
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Text("바로보기님이 지정하신 과제의 3AI 4대 규격(딥서치·뿌리편입·구현확장·AI학습안) 리포트입니다.", color = Color.Gray, fontSize = 12.sp)
                    Spacer(modifier = Modifier.height(12.dp))

                    if (pobbagiReports.isEmpty()) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Icon(Icons.Default.Build, contentDescription = "뽀개기 없음", tint = Color.Gray, modifier = Modifier.size(48.dp))
                                Spacer(modifier = Modifier.height(12.dp))
                                Text("아직 지정된 뽀개기 과제가 없습니다.", color = Color.Gray, fontSize = 14.sp)
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("4번째 [지식 DB] 탭에서 [🔨 뽀개기 지정] 버튼을 눌러보세요.", color = Color(0xFF38BDF8), fontSize = 12.sp)
                            }
                        }
                    } else {
                        LazyColumn(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                            items(pobbagiReports) { report ->
                                val reportAudioUrl = report.audioUrl ?: "/api/v1/knowledge/audio/${report.id}"
                                val isThisPlaying = playingAudioUrl == reportAudioUrl && playingItemId == "POBBAGI_${report.id}"
                                Card(
                                    modifier = Modifier.fillMaxWidth(),
                                    colors = CardDefaults.cardColors(containerColor = Color(0xFF1E1B4B)),
                                    shape = RoundedCornerShape(16.dp)
                                ) {
                                    Column(modifier = Modifier.padding(16.dp)) {
                                        Row(
                                            modifier = Modifier.fillMaxWidth(),
                                            horizontalArrangement = Arrangement.SpaceBetween,
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Surface(
                                                shape = RoundedCornerShape(8.dp),
                                                color = Color(0xFFF43F5E).copy(alpha = 0.2f)
                                            ) {
                                                Text(
                                                    "🔥 3AI 뽀개기 리포트",
                                                    color = Color(0xFFFB7185),
                                                    fontSize = 11.sp,
                                                    fontWeight = FontWeight.Bold,
                                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                                )
                                            }
                                            Surface(
                                                shape = RoundedCornerShape(8.dp),
                                                color = Color(0xFFEAB308).copy(alpha = 0.2f)
                                            ) {
                                                Text(
                                                    "⏳ 만복이 사후 승인 대기중",
                                                    color = Color(0xFFFDE047),
                                                    fontSize = 11.sp,
                                                    fontWeight = FontWeight.SemiBold,
                                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                                )
                                            }
                                        }

                                        Spacer(modifier = Modifier.height(8.dp))
                                        Text(report.title, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                                        Text("지정시각: ${report.designatedAt}\n작성: ${report.author}", color = Color.Gray, fontSize = 11.sp, lineHeight = 15.sp)

                                        Spacer(modifier = Modifier.height(12.dp))

                                        Text("🔍 ① 딥서치 (Deep Search) 분석", color = Color(0xFF38BDF8), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                                        Spacer(modifier = Modifier.height(4.dp))
                                        Text(report.deepSearch, color = Color(0xFFE2E8F0), fontSize = 12.sp, lineHeight = 18.sp)

                                        Spacer(modifier = Modifier.height(10.dp))

                                        Text("🌳 ② 뿌리 체계 편입 방안", color = Color(0xFF4ADE80), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                                        Spacer(modifier = Modifier.height(4.dp))
                                        Text(report.rootIntegration, color = Color(0xFFE2E8F0), fontSize = 12.sp, lineHeight = 18.sp)

                                        Spacer(modifier = Modifier.height(10.dp))

                                        Text("🚀 ③ 구현 후 확장 방안", color = Color(0xFFA855F7), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                                        Spacer(modifier = Modifier.height(4.dp))
                                        Text(report.expansionPlan, color = Color(0xFFE2E8F0), fontSize = 12.sp, lineHeight = 18.sp)

                                        Spacer(modifier = Modifier.height(10.dp))

                                        Text("🧠 ④ AI 학습안 및 프롬프트 반영", color = Color(0xFFF59E0B), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                                        Spacer(modifier = Modifier.height(4.dp))
                                        Text(report.aiLearningPlan, color = Color(0xFFE2E8F0), fontSize = 12.sp, lineHeight = 18.sp)

                                        Spacer(modifier = Modifier.height(14.dp))

                                        Button(
                                            onClick = {
                                                if (isThisPlaying) {
                                                    onStopAudio()
                                                    playingAudioUrl = null
                                                    playingItemId = null
                                                } else {
                                                    onPlayAudio(reportAudioUrl)
                                                    playingAudioUrl = reportAudioUrl
                                                    playingItemId = "POBBAGI_${report.id}"
                                                }
                                            },
                                            colors = ButtonDefaults.buttonColors(
                                                containerColor = if (isThisPlaying) Color(0xFFEF4444) else Color(0xFF0284C7)
                                            ),
                                            modifier = Modifier.fillMaxWidth(),
                                            shape = RoundedCornerShape(8.dp)
                                        ) {
                                            Icon(
                                                imageVector = if (isThisPlaying) Icons.Default.Stop else Icons.Default.PlayArrow,
                                                contentDescription = if (isThisPlaying) "정지" else "재생",
                                                modifier = Modifier.size(16.dp)
                                            )
                                            Spacer(modifier = Modifier.width(6.dp))
                                            Text(if (isThisPlaying) "1분 뽀개기 음성 정지" else "1분 뽀개기 음성 브리핑 듣기", fontSize = 12.sp)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


    // 지식 DB 상세 노하우 다이얼로그 (3-Tier 전체 읽기 및 오디오/유튜브 연결)
    selectedKnowledgeDetailItem?.let { detail ->
        AlertDialog(
            onDismissRequest = { selectedKnowledgeDetailItem = null },
            title = {
                Column {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = Color(0xFF0284C7).copy(alpha = 0.3f)
                        ) {
                            Text(
                                detail.category ?: "지식 DB",
                                color = Color(0xFF38BDF8),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(detail.title, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.White)
                }
            },
            text = {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(max = 450.dp)
                        .verticalScroll(rememberScrollState()),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    detail.keywords?.let { kwList ->
                        if (kwList.isNotEmpty()) {
                            Text(
                                text = kwList.joinToString(" ") { "#$it" },
                                color = Color(0xFFA7F3D0),
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }

                    HorizontalDivider(color = Color(0xFF334155))

                    Text("📖 3-Tier 지식 요약", fontWeight = FontWeight.Bold, fontSize = 14.sp, color = Color(0xFF38BDF8))
                    val summaryText = detail.threeLineSummary ?: detail.snippet ?: ""
                    Text(summaryText, fontSize = 13.sp, color = Color(0xFFCBD5E1), lineHeight = 20.sp)

                    detail.deepInsights?.let { insights ->
                        if (insights.isNotBlank()) {
                            Spacer(modifier = Modifier.height(4.dp))
                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = Color(0xFF334155)
                            ) {
                                Column(modifier = Modifier.padding(10.dp)) {
                                    Text("💡 실전 노하우 (Deep Insights)", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = Color(0xFFFDE047))
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(insights, fontSize = 12.sp, color = Color.White, lineHeight = 18.sp)
                                }
                            }
                        }
                    }

                    detail.sourceUrl?.let { url ->
                        if (url.startsWith("http")) {
                            Spacer(modifier = Modifier.height(4.dp))
                            OutlinedButton(
                                onClick = {
                                    try {
                                        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                                        context.startActivity(intent)
                                    } catch (e: Exception) {
                                        e.printStackTrace()
                                    }
                                },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(8.dp)
                            ) {
                                Icon(Icons.Default.OpenInNew, contentDescription = "원문 보기", modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("유튜브 원문 영상 보기", fontSize = 12.sp)
                            }
                        }
                    }
                }
            },
            confirmButton = {
                val detailAudioUrl = detail.audioUrl ?: "/api/v1/knowledge/audio/${detail.id}"
                val isThisPlaying = playingAudioUrl == detailAudioUrl && playingItemId == detail.id
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Button(
                        onClick = {
                            if (isThisPlaying) {
                                onStopAudio()
                                playingAudioUrl = null
                                playingItemId = null
                            } else {
                                onPlayAudio(detailAudioUrl)
                                playingAudioUrl = detailAudioUrl
                                playingItemId = detail.id
                            }
                        },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (isThisPlaying) Color(0xFFEF4444) else Color(0xFF4ADE80)
                        )
                    ) {
                        Icon(
                            imageVector = if (isThisPlaying) Icons.Default.Stop else Icons.Default.PlayArrow,
                            contentDescription = if (isThisPlaying) "정지" else "재생"
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(if (isThisPlaying) "정지" else "1분 브리핑 듣기")
                    }

                    TextButton(onClick = { selectedKnowledgeDetailItem = null }) {
                        Text("닫기", color = Color.White)
                    }
                }
            },
            containerColor = Color(0xFF1E293B)
        )
    }

    // PLAUD 대체 1-Tap 원터치 실시간 음성 녹음 & 3AI 뽀개기 전송 다이얼로그
    if (showVoiceRecordDialog) {
        var isRecording by remember { mutableStateOf(false) }
        var isSubmitting by remember { mutableStateOf(false) }
        var recordTimeSec by remember { mutableStateOf(0) }
        var mediaRecorder by remember { mutableStateOf<MediaRecorder?>(null) }
        var outputFile by remember { mutableStateOf<File?>(null) }
        var optionalNote by remember { mutableStateOf("") }
        var statusMessage by remember { mutableStateOf("버튼을 누르면 스마트폰 마이크 수음이 시작됩니다.") }

        LaunchedEffect(isRecording) {
            if (isRecording) {
                while (isRecording) {
                    delay(1000L)
                    recordTimeSec++
                }
            }
        }

        DisposableEffect(Unit) {
            onDispose {
                try {
                    mediaRecorder?.stop()
                    mediaRecorder?.release()
                } catch (e: Exception) { }
            }
        }

        val formattedTime = String.format("%02d:%02d", recordTimeSec / 60, recordTimeSec % 60)

        AlertDialog(
            onDismissRequest = {
                if (!isRecording && !isSubmitting) {
                    showVoiceRecordDialog = false
                }
            },
            title = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        Icons.Default.Mic,
                        contentDescription = null,
                        tint = if (isRecording) Color(0xFFEF4444) else Color(0xFFF43F5E),
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("🎙️ PLAUD AI 원터치 음성 녹음", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.White)
                }
            },
            text = {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = if (isRecording) "🔴 음성 녹음 진행 중..." else "스마트폰 마이크로 회의/아이디어를 바로 수음합니다.",
                        fontSize = 12.sp,
                        color = Color(0xFFCBD5E1)
                    )

                    // Timer & Pulse Box
                    Surface(
                        shape = RoundedCornerShape(16.dp),
                        color = if (isRecording) Color(0xFF7F1D1D) else Color(0xFF1E293B),
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp)
                    ) {
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier.padding(16.dp)
                        ) {
                            Text(
                                text = formattedTime,
                                fontSize = 36.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (isRecording) Color(0xFFFCA5A5) else Color(0xFF94A3B8)
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                text = statusMessage,
                                fontSize = 12.sp,
                                color = Color.White
                            )
                        }
                    }

                    // Optional Note text box
                    OutlinedTextField(
                        value = optionalNote,
                        onValueChange = { optionalNote = it },
                        label = { Text("추가 텍스트 메모 (선택사항)") },
                        placeholder = { Text("제목이나 내용을 적지 않아도 자동 수음·분석됩니다.") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                        colors = OutlinedTextFieldDefaults.colors(focusedTextColor = Color.White, unfocusedTextColor = Color.White)
                    )
                }
            },
            confirmButton = {
                Column(modifier = Modifier.fillMaxWidth()) {
                    if (!isRecording && !isSubmitting) {
                        // [🔴 녹음 시작]
                        Button(
                            onClick = {
                                try {
                                    val timeStamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())
                                    val audioFile = File(context.cacheDir, "plaud_rec_$timeStamp.m4a")
                                    outputFile = audioFile

                                    val recorder = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                                        MediaRecorder(context)
                                    } else {
                                        @Suppress("DEPRECATION")
                                        MediaRecorder()
                                    }

                                    recorder.setAudioSource(MediaRecorder.AudioSource.MIC)
                                    recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
                                    recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
                                    recorder.setOutputFile(audioFile.absolutePath)
                                    recorder.prepare()
                                    recorder.start()

                                    mediaRecorder = recorder
                                    recordTimeSec = 0
                                    isRecording = true
                                    statusMessage = "🔴 마이크 수음 중... 말씀하세요."
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                    statusMessage = "녹음 시작 오류: ${e.message}"
                                }
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFEF4444)),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Icon(Icons.Default.RadioButtonChecked, contentDescription = null)
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("🔴 녹음 시작", fontWeight = FontWeight.Bold)
                        }
                    } else if (isRecording) {
                        // [⏹️ 녹음 종료 및 3AI 전송]
                        Button(
                            onClick = {
                                try {
                                    mediaRecorder?.stop()
                                    mediaRecorder?.release()
                                    mediaRecorder = null
                                    isRecording = false
                                    statusMessage = "⏹️ 녹음 완료! 3AI 인제스트 전송 중..."
                                    isSubmitting = true

                                    scope.launch {
                                        val timeStr = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault()).format(Date())
                                        val titleText = if (optionalNote.isNotBlank()) optionalNote else "PLAUD 음성 메모 ($timeStr)"
                                        
                                        var base64Data: String? = null
                                        outputFile?.let { file ->
                                            if (file.exists()) {
                                                val bytes = file.readBytes()
                                                base64Data = Base64.encodeToString(bytes, Base64.NO_WRAP)
                                            }
                                        }

                                        repository.recordVoiceIngest(titleText, "스마트폰 마이크 음성 수음 레코딩", base64Data).onSuccess {
                                            showVoiceRecordDialog = false
                                            selectedTab = 4
                                            repository.fetchPobbagiResults().onSuccess { pobbagiReports = it }
                                        }
                                        isSubmitting = false
                                    }
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                    isRecording = false
                                    isSubmitting = false
                                    statusMessage = "녹음 종료 실패: ${e.message}"
                                }
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF38BDF8)),
                            modifier = Modifier.fillMaxWidth(),
                            enabled = !isSubmitting
                        ) {
                            Icon(Icons.Default.Stop, contentDescription = null)
                            Spacer(modifier = Modifier.width(6.dp))
                            Text(if (isSubmitting) "전송 중..." else "⏹️ 녹음 종료 & 3AI 뽀개기 자동 전송", fontWeight = FontWeight.Bold)
                        }
                    }
                }
            },
            dismissButton = {
                if (!isSubmitting) {
                    TextButton(onClick = {
                        try {
                            mediaRecorder?.stop()
                            mediaRecorder?.release()
                        } catch (e: Exception) { }
                        mediaRecorder = null
                        isRecording = false
                        showVoiceRecordDialog = false
                    }) {
                        Text("취소", color = Color.Gray)
                    }
                }
            },
            containerColor = Color(0xFF1E1B4B)
        )
    }

    // 서버 설정 다이얼로그 (수동 편집 및 즉시 자동 감지 지원)
    if (showSettingsDialog) {
        var internalInput by remember { mutableStateOf(ServerConfig.getInternalUrl(context)) }
        var externalInput by remember { mutableStateOf(ServerConfig.getExternalUrl(context)) }

        AlertDialog(
            onDismissRequest = { showSettingsDialog = false },
            title = { Text("서버 접속 환경 설정", fontWeight = FontWeight.Bold) },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("집 Wi-Fi (내부 사설 IP):", fontSize = 12.sp, color = Color.Gray)
                    OutlinedTextField(
                        value = internalInput,
                        onValueChange = { internalInput = it },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth()
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    Text("모바일 LTE / 외부망 (Cloudflare 터널):", fontSize = 12.sp, color = Color.Gray)
                    OutlinedTextField(
                        value = externalInput,
                        onValueChange = { externalInput = it },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth()
                    )

                    Spacer(modifier = Modifier.height(8.dp))
                    Button(
                        onClick = {
                            ServerConfig.saveUrls(context, internalInput, externalInput)
                            scope.launch {
                                isCheckingNetwork = true
                                isExternal = ServerConfig.autoDetectAndSwitch(context)
                                isCheckingNetwork = false
                                repository.fetchLatestBriefing().onSuccess { latestBriefing = it }
                                repository.fetchKnowledgeList().onSuccess { knowledgeList = it }
                                repository.fetchChatHistory().onSuccess { chatMessages = it }
                                showSettingsDialog = false
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0284C7)),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("지금 즉시 네트워크 자동 감지 및 저장")
                    }
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        ServerConfig.saveUrls(context, internalInput, externalInput)
                        scope.launch {
                            isCheckingNetwork = true
                            isExternal = ServerConfig.autoDetectAndSwitch(context)
                            isCheckingNetwork = false
                            repository.fetchLatestBriefing().onSuccess { latestBriefing = it }
                            repository.fetchKnowledgeList().onSuccess { knowledgeList = it }
                            repository.fetchChatHistory().onSuccess { chatMessages = it }
                            showSettingsDialog = false
                        }
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0284C7))
                ) {
                    Text("저장 및 적용")
                }
            }
        )
    }
}
