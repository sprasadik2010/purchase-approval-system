import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:pull_to_refresh/pull_to_refresh.dart';
import 'package:flutter_staggered_animations/flutter_staggered_animations.dart';
import '../providers/request_provider.dart';
import '../widgets/request_card.dart';
import '../widgets/stats_card.dart';
import '../screens/request_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final RefreshController _refreshController = RefreshController();
  String _selectedFilter = 'all';

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<RequestProvider>().loadRequests();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Consumer<RequestProvider>(
        builder: (context, provider, child) {
          final filteredRequests = provider.getFilteredRequests(_selectedFilter);
          final stats = provider.getStats();

          return SmartRefresher(
            controller: _refreshController,
            onRefresh: () async {
              await provider.loadRequests();
              _refreshController.refreshCompleted();
            },
            child: CustomScrollView(
              slivers: [
                SliverAppBar(
                  expandedHeight: 140,
                  floating: true,
                  pinned: true,
                  flexibleSpace: FlexibleSpaceBar(
                    title: const Text(
                      'Purchase Requests',
                      style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                    background: Container(
                      decoration: const BoxDecoration(
                        gradient: LinearGradient(
                          colors: [Colors.blue, Colors.indigo],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                      ),
                    ),
                  ),
                ),
                SliverPadding(
                  padding: const EdgeInsets.all(16),
                  sliver: SliverList(
                    delegate: SliverChildListDelegate([
                      // Stats cards
                      Row(
                        children: [
                          Expanded(
                            child: StatsCard(
                              title: 'Total',
                              value: stats['total'] ?? 0,
                              color: Colors.blue,
                              icon: Icons.list_alt,
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: StatsCard(
                              title: 'Pending',
                              value: stats['pending'] ?? 0,
                              color: Colors.orange,
                              icon: Icons.hourglass_empty,
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: StatsCard(
                              title: 'Approved',
                              value: stats['approved'] ?? 0,
                              color: Colors.green,
                              icon: Icons.check_circle,
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: StatsCard(
                              title: 'Rejected',
                              value: stats['rejected'] ?? 0,
                              color: Colors.red,
                              icon: Icons.cancel,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      // Filter chips
                      Wrap(
                        spacing: 8,
                        children: ['all', 'pending', 'approved', 'rejected'].map((filter) {
                          return FilterChip(
                            label: Text(filter.toUpperCase()),
                            selected: _selectedFilter == filter,
                            onSelected: (selected) {
                              setState(() {
                                _selectedFilter = filter;
                              });
                            },
                            backgroundColor: Colors.grey[200],
                            selectedColor: Colors.blue[100],
                            checkmarkColor: Colors.blue,
                          );
                        }).toList(),
                      ),
                      const SizedBox(height: 16),
                      // Requests list
                      provider.isLoading
                          ? const Center(
                              child: Padding(
                                padding: EdgeInsets.all(32),
                                child: CircularProgressIndicator(),
                              ),
                            )
                          : filteredRequests.isEmpty
                              ? const Center(
                                  child: Padding(
                                    padding: EdgeInsets.all(32),
                                    child: Text('No requests found'),
                                  ),
                                )
                              : AnimationLimiter(
                                  child: Column(
                                    children: AnimationConfiguration.toStaggeredList(
                                      duration: const Duration(milliseconds: 500),
                                      childAnimationBuilder: (widget) => SlideAnimation(
                                        horizontalOffset: 50,
                                        child: FadeInAnimation(
                                          child: widget,
                                        ),
                                      ),
                                      children: filteredRequests.map((request) {
                                        return RequestCard(
                                          request: request,
                                          onTap: () {
                                            Navigator.pushNamed(
                                              context,
                                              '/request-detail',
                                              arguments: request.id,
                                            ).then((_) => provider.loadRequests());
                                          },
                                        );
                                      }).toList(),
                                    ),
                                  ),
                                ),
                    ]),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}