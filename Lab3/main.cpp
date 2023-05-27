#include <iostream>
#include <list>
#include <map>

// 152120161061 Mithat Uçar
// 152117107_2223G_Lab_Uygulama3 Artificial Intelligence

using namespace std;

class Graph
{
  int V;
  map<string, list<string>> adj;

public:
  Graph(int V);

  // function to add an edge to graph
  void addEdge(string v, string w);

  // prints BFS traversal from a start node
  void BFS(string s);
};

Graph::Graph(int V)
{
  this->V = V;
}

void Graph::addEdge(string v, string w)
{
  adj[v].push_back(w);
}

void Graph::BFS(string s)
{
  map<string, bool> visited;

  // Create a queue for output
  list<string> queue;

  // Mark the current node as visited and enqueue it
  visited[s] = true;
  queue.push_back(s);

  while (!queue.empty())
  {
    // Dequeue a vertex from queue and print it
    s = queue.front();
    cout << s << " ";
    queue.pop_front();

    // Check a node adjecent nodes if not visited push that to the queue
    for (auto adjecent : adj[s])
    {
      if (!visited[adjecent])
      {
        visited[adjecent] = true;
        queue.push_back(adjecent);
      }
    }
  }
}

int main()
{
  Graph g(6);
  g.addEdge("a", "b");
  g.addEdge("a", "e");
  g.addEdge("b", "c");
  g.addEdge("b", "d");
  g.addEdge("c", "b");
  g.addEdge("c", "d");
  g.addEdge("d", "b");
  g.addEdge("d", "c");
  g.addEdge("e", "f");

  cout << "Breadth First Traversal Starting From node a \n";
  g.BFS("a");

  return 0;
}