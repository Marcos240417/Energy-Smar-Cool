import React from 'react';
import { Thermometer, Droplets, AlertTriangle, CheckCircle } from 'lucide-react';

const SensorCard = ({ sensor }) => {
  const isHighTemp = sensor.temperatura > 10; // Exemplo de lógica de alerta

  return (
    <div className={`bg-white p-6 rounded-2xl shadow-lg border-l-8 transition-all hover:shadow-xl ${isHighTemp ? 'border-red-500' : 'border-blue-500'}`}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-slate-800 font-bold text-lg">{sensor.nome || 'Sensor s/ nome'}</h3>
          <p className="text-slate-400 text-xs font-mono">{sensor.mac}</p>
        </div>
        {isHighTemp ? (
          <AlertTriangle className="text-red-500 w-6 h-6 animate-pulse" />
        ) : (
          <CheckCircle className="text-green-500 w-6 h-6" />
        )}
      </div>

      <div className="grid grid-cols-2 gap-4 mt-6">
        <div className="flex items-center gap-2">
          <div className="bg-blue-50 p-2 rounded-lg">
            <Thermometer className="text-blue-600 w-5 h-5" />
          </div>
          <div>
            <p className="text-slate-400 text-[10px] uppercase font-bold">Temp.</p>
            <p className="text-xl font-bold text-slate-700">{sensor.temperatura}°C</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="bg-cyan-50 p-2 rounded-lg">
            <Droplets className="text-cyan-600 w-5 h-5" />
          </div>
          <div>
            <p className="text-slate-400 text-[10px] uppercase font-bold">Umidade</p>
            <p className="text-xl font-bold text-slate-700">{sensor.umidade}%</p>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-slate-50 flex justify-between items-center">
        <span className={`text-[10px] font-bold px-2 py-1 rounded-full ${sensor.status === 'online' ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-500'}`}>
          {sensor.status?.toUpperCase() || 'OFFLINE'}
        </span>
        <span className="text-slate-300 text-[10px]">visto há 2 min</span>
      </div>
    </div>
  );
};

export default SensorCard;