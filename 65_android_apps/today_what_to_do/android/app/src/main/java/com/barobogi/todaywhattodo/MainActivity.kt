package com.barobogi.todaywhattodo

import android.Manifest
import android.content.pm.PackageManager
import android.location.Geocoder
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.barobogi.todaywhattodo.data.model.Place
import com.barobogi.todaywhattodo.ui.screens.*
import com.barobogi.todaywhattodo.ui.theme.TodayWhatToDoTheme
import com.barobogi.todaywhattodo.viewmodel.RecommendViewModel
import com.google.android.gms.location.LocationServices
import java.util.Locale

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            TodayWhatToDoTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    TodayWhatToDoApp()
                }
            }
        }
    }
}

sealed class BottomNavItem(val route: String, val title: String, val icon: String) {
    object Home : BottomNavItem("home", "홈", "🏠")
    object Condition : BottomNavItem("condition/7세 아이", "맞춤추천", "🎯")
    object Saved : BottomNavItem("saved", "저장", "⭐")
    object MyPage : BottomNavItem("mypage", "마이", "👤")
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TodayWhatToDoApp(viewModel: RecommendViewModel = viewModel()) {
    val navController = rememberNavController()
    val selectedPlace = remember { mutableStateOf<Place?>(null) }
    val context = LocalContext.current

    // GPS 위치 수집 및 권한 처리
    val locationPermissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        val granted = permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true ||
                permissions[Manifest.permission.ACCESS_COARSE_LOCATION] == true
        if (granted) {
            fetchDeviceLocation(context, viewModel)
        } else {
            viewModel.updateLocation(37.5665, 126.9780, "서울 중구 (위치 권한 미승인)")
        }
    }

    LaunchedEffect(Unit) {
        val hasFine = ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
        val hasCoarse = ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED
        if (hasFine || hasCoarse) {
            fetchDeviceLocation(context, viewModel)
        } else {
            locationPermissionLauncher.launch(
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                )
            )
        }
    }

    val bottomItems = listOf(
        BottomNavItem.Home,
        BottomNavItem.Condition,
        BottomNavItem.Saved,
        BottomNavItem.MyPage
    )
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    Scaffold(
        bottomBar = {
            NavigationBar {
                bottomItems.forEach { item ->
                    val isSelected = currentRoute == item.route || (item is BottomNavItem.Condition && currentRoute?.startsWith("condition") == true)
                    NavigationBarItem(
                        selected = isSelected,
                        onClick = {
                            navController.navigate(item.route) {
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        icon = { Text(item.icon) },
                        label = { Text(item.title) }
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(innerPadding)
        ) {
            composable("home") {
                HomeScreen(
                    viewModel = viewModel,
                    onNavigateToCondition = { companion ->
                        navController.navigate("condition/$companion")
                    },
                    onNavigateToSaved = { navController.navigate("saved") },
                    onNavigateToMyPage = { navController.navigate("mypage") }
                )
            }
            composable("condition/{companion}") { backStackEntry ->
                val companion = backStackEntry.arguments?.getString("companion") ?: "7세 아이"
                ConditionInputScreen(
                    initialCompanion = companion,
                    viewModel = viewModel,
                    onNavigateToResult = {
                        navController.navigate("result")
                    },
                    onBack = { navController.popBackStack() }
                )
            }
            composable("result") {
                ResultScreen(
                    viewModel = viewModel,
                    onPlaceClick = { place ->
                        selectedPlace.value = place
                        navController.navigate("detail")
                    },
                    onBack = { navController.popBackStack() }
                )
            }
            composable("detail") {
                selectedPlace.value?.let { place ->
                    DetailScreen(
                        place = place,
                        onBack = { navController.popBackStack() }
                    )
                }
            }
            composable("saved") {
                SavedScreen(onBack = { navController.popBackStack() })
            }
            composable("mypage") {
                MyPageScreen(onBack = { navController.popBackStack() })
            }
        }
    }
}

private fun fetchDeviceLocation(context: android.content.Context, viewModel: RecommendViewModel) {
    try {
        val fusedClient = LocationServices.getFusedLocationProviderClient(context)
        fusedClient.lastLocation.addOnSuccessListener { loc ->
            if (loc != null) {
                val lat = loc.latitude
                val lon = loc.longitude
                var name = "현재 위치"
                try {
                    val geocoder = Geocoder(context, Locale.KOREA)
                    @Suppress("DEPRECATION")
                    val addresses = geocoder.getFromLocation(lat, lon, 1)
                    if (!addresses.isNullOrEmpty()) {
                        val addr = addresses[0]
                        val admin = addr.locality ?: addr.adminArea ?: ""
                        val subAdmin = addr.subLocality ?: addr.thoroughfare ?: ""
                        name = "$admin $subAdmin".trim().ifBlank { "현재 위치" }
                    }
                } catch (e: Exception) {
                    name = "현재 위치 (${String.format("%.2f", lat)}, ${String.format("%.2f", lon)})"
                }
                viewModel.updateLocation(lat, lon, name)
            } else {
                viewModel.updateLocation(37.5665, 126.9780, "서울 중구 (GPS 신호 대기)")
            }
        }.addOnFailureListener {
            viewModel.updateLocation(37.5665, 126.9780, "서울 중구 (GPS 감지 실패)")
        }
    } catch (e: SecurityException) {
        viewModel.updateLocation(37.5665, 126.9780, "서울 중구 (위치 권한 오류)")
    }
}
