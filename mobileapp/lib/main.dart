import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/request_provider.dart';
import 'screens/home_screen.dart';
import 'screens/request_detail_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => RequestProvider()),
      ],
      child: MaterialApp(
        title: 'Purchase Approval',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          useMaterial3: true,
        ),
        home: const HomeScreen(),
        onGenerateRoute: (settings) {
          if (settings.name == '/request-detail') {
            final args = settings.arguments as int;
            return MaterialPageRoute(
              builder: (context) => RequestDetailScreen(requestId: args),
            );
          }
          return null;
        },
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}