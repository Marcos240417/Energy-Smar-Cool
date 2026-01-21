import React, { useState } from 'react';
import Login from './pages/Login';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('access_token'));

  if (!isAuthenticated) {
    return <Login onLoginSuccess={() => setIsAuthenticated(true)} />;
  }

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold text-slate-800">Painel de Monitoramento</h1>
          <button 
            onClick={() => { localStorage.clear(); setIsAuthenticated(false); }}
            className="text-slate-500 hover:text-red-600 font-medium"
          >
            Sair
          </button>
        </header>
        
        {/* Aqui entrarão os nossos Cards e Gráficos */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
            <h3 className="text-slate-500 text-sm font-bold uppercase">Sensores Ativos</h3>
            <p className="text-3xl font-bold text-blue-600">Carregando...</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;