#include <bits/stdc++.h>
using namespace std;

bool isSafe(int node, vector<vector<int>>& graph, vector<int>& color, int c, int n){
    for(int k = 0; k < n; k++){
        if(graph[node][k] == 1 && color[k] == c)
            return false;
    }
    return true;
}

bool solve(int node, vector<vector<int>>& graph, int m, int n, vector<int>& color){
    if(node == n) return true;

    for(int c = 1; c <= m; c++){
        if(isSafe(node, graph, color, c, n)){
            color[node] = c;
            
            if(solve(node+1, graph, m, n, color))
                return true;
            color[node] = 0;
        }
    }
    return false;
}

int main(){
    int n, m;
    cin >> n >> m;

    vector<vector<int>> graph(n, vector<int>(n));

    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            cin >> graph[i][j];
        }
    }

    vector<int> color(n, 0);

    if(solve(0, graph, m, n, color)){
        for(int i=0;i<n;i++){
            cout << color[i] << " ";
        }
    } else {
        cout << "NO";
    }

    return 0;
}