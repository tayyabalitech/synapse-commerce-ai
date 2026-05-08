'use client';

export const dynamic = 'force-dynamic';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import ActionCard from '@/components/ActionCard';

const SUPPORTED_COUNTRIES = [
  { label: "United States 🇺🇸", code: "us", trends: "united_states" },
  { label: "United Kingdom 🇬🇧", code: "uk", trends: "united_kingdom" },
  { label: "Canada 🇨🇦", code: "ca", trends: "canada" },
  { label: "Australia 🇦🇺", code: "au", trends: "australia" },
  { label: "Germany 🇩🇪", code: "de", trends: "germany" },
  { label: "France 🇫🇷", code: "fr", trends: "france" },
  { label: "Japan 🇯🇵", code: "jp", trends: "japan" },
  { label: "Brazil 🇧🇷", code: "br", trends: "brazil" },
  { label: "India 🇮🇳", code: "in", trends: "india" }
];

export default function Dashboard() {
  const [actions, setActions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCountry, setSelectedCountry] = useState(SUPPORTED_COUNTRIES[0]);
  const [discoveryLoading, setDiscoveryLoading] = useState(false);

  useEffect(() => {
    fetchActions();
  }, []);

  async function fetchActions() {
    setLoading(true);
    const { data, error } = await supabase
      .from('pending_actions')
      .select('*')
      .eq('status', 'pending')
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching actions:', error);
    } else {
      setActions(data || []);
    }
    setLoading(false);
  }

  const handleApprove = async (id: string) => {
    try {
      setLoading(true);
      // Trigger the real-world execution on our Python backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/approve/${id}`, {
        method: 'POST',
      });

      if (response.ok) {
        alert('Successfully published to WooCommerce!');
        fetchActions();
      } else {
        const err = await response.json();
        alert('Failed to publish: ' + err.detail);
      }
    } catch (error) {
      console.error('Approval error:', error);
      alert('Error connecting to backend server.');
    } finally {
      setLoading(false);
    }
  };

  const handleRunDiscovery = async () => {
    try {
      setDiscoveryLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/run-discovery`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          country_code: selectedCountry.code,
          trends_region: selectedCountry.trends
        })
      });

      if (response.ok) {
        alert(`AI Discovery Agent triggered for ${selectedCountry.label}!`);
      } else {
        alert('Failed to start discovery.');
      }
    } catch (error) {
      console.error('Discovery error:', error);
      alert('Error connecting to backend server.');
    } finally {
      setDiscoveryLoading(false);
    }
  };


  const handleReject = async (id: string) => {
    const { error } = await supabase
      .from('pending_actions')
      .update({ status: 'rejected' })
      .eq('id', id);
    
    if (error) {
      alert('Failed to reject action: ' + error.message);
    } else {
      fetchActions();
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white p-8 md:p-16 lg:p-24 selection:bg-blue-500/30">
      <div className="max-w-6xl mx-auto">
        <header className="mb-20 flex flex-col md:flex-row justify-between items-start md:items-end gap-8">
          <div className="space-y-4">
            <div className="inline-flex items-center gap-3 px-4 py-1.5 rounded-full bg-white/5 border border-white/10">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
              </span>
              <span className="text-[10px] font-black uppercase tracking-[0.3em] text-blue-100/60">System Online</span>
            </div>
            <h1 className="text-6xl font-black tracking-tight leading-tight">
              Synapse<span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600">Commerce</span>
            </h1>
            <p className="text-gray-500 font-light max-w-md text-lg leading-relaxed">
              Human-in-the-Loop AI Orchestration. Approve or reject autonomous product discoveries.
            </p>
          </div>
          
          <div className="flex flex-col items-end gap-6">
            <div className="flex items-center gap-3">
              <select 
                value={selectedCountry.code}
                onChange={(e) => {
                  const country = SUPPORTED_COUNTRIES.find(c => c.code === e.target.value);
                  if (country) setSelectedCountry(country);
                }}
                className="bg-white/5 border border-white/10 text-white rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-500 cursor-pointer"
              >
                {SUPPORTED_COUNTRIES.map(country => (
                  <option key={country.code} value={country.code} className="bg-[#0a0a0a]">
                    {country.label}
                  </option>
                ))}
              </select>
              
              <button 
                onClick={handleRunDiscovery}
                disabled={discoveryLoading}
                className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white px-5 py-2 rounded-lg text-sm font-bold tracking-wide transition-colors shadow-lg shadow-blue-500/20 flex items-center gap-2"
              >
                {discoveryLoading ? (
                  <span className="animate-pulse">Starting...</span>
                ) : (
                  <>
                    <span>Run AI Agent</span>
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </>
                )}
              </button>
            </div>
            
            <button 
              onClick={fetchActions}
              className="group flex flex-col items-end gap-2 outline-none"
            >
              <span className="text-[10px] font-bold uppercase tracking-widest text-gray-500 group-hover:text-white transition-colors">Sync Database</span>
              <div className="w-12 h-[1px] bg-white/10 group-hover:w-24 group-hover:bg-blue-500 transition-all duration-500" />
            </button>
          </div>
        </header>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-[400px] rounded-2xl bg-white/5 animate-pulse border border-white/5" />
            ))}
          </div>
        ) : actions.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {actions.map((action) => (
              <ActionCard
                key={action.id}
                action={action}
                onApprove={handleApprove}
                onReject={handleReject}
              />
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-40 bg-white/[0.02] rounded-3xl border border-dashed border-white/10">
            <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mb-6">
              <svg className="w-8 h-8 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
            </div>
            <p className="text-gray-500 font-medium tracking-wide uppercase text-[10px]">Queue is currently empty</p>
          </div>
        )}
      </div>
    </main>
  );
}
