const HandoffQueue = () => {
  return (
    <div className="w-full">
      <div className="flex justify-between items-end mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 tracking-tight">Handoff Queue</h2>
          <p className="text-sm text-gray-500 mt-1">Sunrise Clinic, Dehradun — conversations the agent escalated</p>
        </div>
        <button className="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded tracking-wide uppercase">4 OPEN</button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-5 rounded-lg border border-gray-200 shadow-sm">
          <div className="text-[10px] text-gray-400 font-bold mb-2 uppercase tracking-wider">Conversations</div>
          <div className="text-3xl font-bold text-gray-800">37</div>
          <div className="text-[11px] text-gray-400 mt-1">today</div>
        </div>
        <div className="bg-white p-5 rounded-lg border border-gray-200 shadow-sm">
          <div className="text-[10px] text-gray-400 font-bold mb-2 uppercase tracking-wider">Completed By Agent</div>
          <div className="text-3xl font-bold text-gray-800">31</div>
          <div className="text-[11px] text-gray-400 mt-1">84%</div>
        </div>
        <div className="bg-white p-5 rounded-lg border border-gray-200 shadow-sm">
          <div className="text-[10px] text-gray-400 font-bold mb-2 uppercase tracking-wider">Escalated</div>
          <div className="text-3xl font-bold text-gray-800">6</div>
          <div className="text-[11px] text-blue-500 font-medium mt-1">4 still open</div>
        </div>
        <div className="bg-white p-5 rounded-lg border border-red-200 shadow-sm">
          <div className="text-[10px] text-gray-400 font-bold mb-2 uppercase tracking-wider">Urgent</div>
          <div className="text-3xl font-bold text-gray-800">1</div>
          <div className="text-[11px] text-red-500 font-medium mt-1">clinical, unresolved</div>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
        <div className="text-sm font-bold text-gray-800 p-5 border-b border-gray-100">
          Open handoffs
        </div>
        <table className="w-full text-left text-sm">
          <thead className="text-[10px] text-gray-400 uppercase tracking-widest font-bold">
            <tr>
              <th className="px-5 py-4 w-32">Conversation</th>
              <th className="px-5 py-4">Caller Said</th>
              <th className="px-5 py-4">Reason</th>
              <th className="px-5 py-4 w-24">Time</th>
              <th className="px-5 py-4 w-24"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 text-sm">
            <tr className="hover:bg-gray-50/50">
              <td className="px-5 py-4 text-gray-500 font-mono text-[11px]">cv_4471</td>
              <td className="px-5 py-4 font-semibold text-gray-800">"Seene mein dard ho raha hai"</td>
              <td className="px-5 py-4">
                <span className="text-red-700 bg-red-50 border border-red-100 px-2 py-0.5 rounded text-[10px] font-bold tracking-wider">CLINICAL</span>
              </td>
              <td className="px-5 py-4 text-gray-500 text-[13px]">11:42</td>
              <td className="px-5 py-4 text-right">
                <button className="bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-bold px-4 py-1.5 rounded shadow-sm transition-colors">Resolve</button>
              </td>
            </tr>
            <tr className="hover:bg-gray-50/50">
              <td className="px-5 py-4 text-gray-500 font-mono text-[11px]">cv_4468</td>
              <td className="px-5 py-4 font-semibold text-gray-800">Cancel for a different patient</td>
              <td className="px-5 py-4">
                <span className="text-orange-700 bg-orange-50 border border-orange-100 px-2 py-0.5 rounded text-[10px] font-bold tracking-wider">NOT AUTHORISED</span>
              </td>
              <td className="px-5 py-4 text-gray-500 text-[13px]">11:20</td>
              <td className="px-5 py-4 text-right">
                <button className="border border-gray-300 hover:bg-gray-50 text-gray-600 text-[11px] font-bold px-4 py-1.5 rounded shadow-sm transition-colors">Resolve</button>
              </td>
            </tr>
            <tr className="hover:bg-gray-50/50">
              <td className="px-5 py-4 text-gray-500 font-mono text-[11px]">cv_4463</td>
              <td className="px-5 py-4 font-semibold text-gray-800">"Sharma ji ke liye" — 3 matches</td>
              <td className="px-5 py-4">
                <span className="text-yellow-700 bg-yellow-50 border border-yellow-100 px-2 py-0.5 rounded text-[10px] font-bold tracking-wider">AMBIGUOUS PATIENT</span>
              </td>
              <td className="px-5 py-4 text-gray-500 text-[13px]">10:57</td>
              <td className="px-5 py-4 text-right">
                <button className="border border-gray-300 hover:bg-gray-50 text-gray-600 text-[11px] font-bold px-4 py-1.5 rounded shadow-sm transition-colors">Resolve</button>
              </td>
            </tr>
            <tr className="hover:bg-gray-50/50">
              <td className="px-5 py-4 text-gray-500 font-mono text-[11px]">cv_4455</td>
              <td className="px-5 py-4 font-semibold text-gray-800">"Ye dawai lun ya nahi?"</td>
              <td className="px-5 py-4">
                <span className="text-red-700 bg-red-50 border border-red-100 px-2 py-0.5 rounded text-[10px] font-bold tracking-wider">MEDICAL ADVICE</span>
              </td>
              <td className="px-5 py-4 text-gray-500 text-[13px]">10:18</td>
              <td className="px-5 py-4 text-right">
                <button className="border border-gray-300 hover:bg-gray-50 text-gray-600 text-[11px] font-bold px-4 py-1.5 rounded shadow-sm transition-colors">Resolve</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HandoffQueue;
