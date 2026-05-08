'use client';

import React from 'react';

interface ActionCardProps {
  action: {
    id: string;
    agent_name: string;
    action_type: string;
    payload: any;
    status: string;
    created_at: string;
  };
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
}

const ActionCard: React.FC<ActionCardProps> = ({ action, onApprove, onReject }) => {
  // Defensive check for payload
  const payload = action.payload || {};
  const { product_name, price, description } = payload;

  return (
    <div className="glass rounded-2xl p-6 shadow-2xl border border-white/5 bg-white/[0.02] backdrop-blur-xl hover:bg-white/[0.04] transition-all duration-300 group">
      <div className="flex justify-between items-start mb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
            <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-blue-400/80">
              {action.agent_name.replace('_', ' ')}
            </span>
          </div>
          <h3 className="text-xl font-semibold text-white group-hover:text-blue-200 transition-colors">
            {product_name || 'Unnamed Product'}
          </h3>
        </div>
        <div className="text-right">
          <div className="text-2xl font-light tracking-tighter text-white">
            <span className="text-sm align-top mr-0.5 opacity-50">$</span>
            {price || '0.00'}
          </div>
          <p className="text-[9px] font-medium text-gray-500 uppercase tracking-widest mt-1">
            {new Date(action.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>

      <div className="relative mb-8">
        <div 
          className="text-xs leading-relaxed text-gray-400 line-clamp-4 font-light overflow-hidden"
          dangerouslySetInnerHTML={{ __html: description || 'No description provided.' }}
        />
        <div className="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-[#0a0a0a]/50 to-transparent pointer-events-none" />
      </div>

      <div className="flex gap-4">
        <button
          onClick={() => onApprove(action.id)}
          className="flex-1 relative overflow-hidden bg-white text-black text-xs font-bold py-4 rounded-lg hover:bg-gray-200 active:scale-95 transition-all shadow-[0_0_20px_rgba(255,255,255,0.1)]"
        >
          APPROVE
        </button>
        <button
          onClick={() => onReject(action.id)}
          className="px-6 bg-transparent text-gray-500 text-[10px] font-bold rounded-lg border border-white/10 hover:border-red-500/50 hover:text-red-400 transition-all uppercase tracking-widest active:scale-95"
        >
          Reject
        </button>
      </div>
    </div>
  );
};

export default ActionCard;
