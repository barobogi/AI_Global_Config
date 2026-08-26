package com.barobogi.todaywhattodo

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.barobogi.todaywhattodo.data.model.Place
import com.barobogi.todaywhattodo.ui.screens.ConditionInputScreen
import com.barobogi.todaywhattodo.ui.screens.DetailScreen
import com.barobogi.todaywhattodo.ui.screens.HomeScreen
import com.barobogi.todaywhattodo.ui.screens.MyPageScreen
import com.barobogi.todaywhattodo.ui.screens.ResultScreen
import com.barobogi.todaywhattodo.ui.screens.SavedScreen
import com.barobogi.todaywhattodo.ui.theme.TodayWhatToDoTheme
import com.barobogi.todaywhattodo.viewmodel.RecommendViewModel
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember

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

@Composable
fun TodayWhatToDoApp(viewModel: RecommendViewModel = viewModel()) {
    val navController = rememberNavController()
    val selectedPlace = remember { mutableStateOf<Place?>(null) }

    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(
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

