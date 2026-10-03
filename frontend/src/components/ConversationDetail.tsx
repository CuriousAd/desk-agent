const ConversationDetail = () => {
  return (
    <div className="w-full">
      <div className="flex justify-between items-end mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 tracking-tight">Conversation cv_4471</h2>
          <p className="text-sm text-gray-500 mt-1">Sunrise Clinic, Dehradun — 27 Sep 2026, 11:42</p>
        </div>
        <div className="text-[10px] font-bold text-red-700 bg-red-50 border border-red-100 px-3 py-1.5 rounded tracking-widest uppercase">
          ESCALATED — CLINICAL
        </div>
      </div>

      <div className="flex gap-6 items-start">
        {/* Transcript Area */}
        <div className="flex-[2] bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <h3 className="text-sm font-bold text-gray-800 mb-8">Transcript and tool calls</h3>
          
          <div className="space-y-6">
            <div className="flex gap-5">
              <div className="w-12 text-[10px] font-bold text-gray-400 text-right pt-2.5 uppercase tracking-widest">Caller</div>
              <div className="bg-gray-50 border border-gray-100 text-gray-800 px-4 py-2.5 rounded-lg text-sm rounded-tl-sm w-full font-medium">
                Kal subah ka appointment mil jayega Dr. Rao ke saath?
              </div>
            </div>

            <div className="flex gap-5">
              <div className="w-12 text-[10px] font-bold text-gray-400 text-right pt-2.5 uppercase tracking-widest">Tool</div>
              <div className="bg-blue-50/50 border border-blue-100 rounded text-[11px] font-mono p-3.5 text-gray-500 w-full leading-relaxed">
                <span className="font-bold text-gray-800">search_slots</span>(doctor_id="dr_rao", date="2026-09-28", window="morning")<br/>
                <span className="text-blue-600 font-semibold mt-1 inline-block">↳ 3 slots: 09:30, 10:15, 11:00</span>
              </div>
            </div>

            <div className="flex gap-5">
              <div className="w-12 text-[10px] font-bold text-gray-400 text-right pt-2.5 uppercase tracking-widest">Agent</div>
              <div className="bg-white border border-gray-200 shadow-sm text-gray-800 px-4 py-2.5 rounded-lg text-sm rounded-tl-sm w-full font-medium">
                Ji, kal subah 9:30, 10:15 aur 11:00 khali hai. Kaun sa theek rahega?
              </div>
            </div>

            <div className="flex gap-5">
              <div className="w-12 text-[10px] font-bold text-gray-400 text-right pt-2.5 uppercase tracking-widest">Caller</div>
              <div className="bg-gray-50 border border-gray-100 text-gray-800 px-4 py-2.5 rounded-lg text-sm rounded-tl-sm w-full font-medium">
                10:15 kar dijiye. Waise abhi seene mein dard ho raha hai thoda.
              </div>
            </div>

            <div className="flex gap-5 relative">
              {/* Vertical red line connector */}
              <div className="absolute left-[88px] top-8 bottom-[-24px] w-[2px] bg-red-100 -z-10"></div>
              
              <div className="w-12 text-[10px] font-bold text-gray-400 text-right pt-2.5 uppercase tracking-widest bg-white">Tool</div>
              <div className="bg-red-50/50 border border-red-100 rounded text-[11px] font-mono p-3.5 text-gray-500 w-full z-10 leading-relaxed">
                <span className="font-bold text-gray-800">escalate_to_human</span>(reason="clinical_urgent",<br/>
                detail="caller reports active chest pain")
              </div>
            </div>

            <div className="flex gap-5">
              <div className="w-12 text-[10px] font-bold text-gray-400 text-right pt-2.5 uppercase tracking-widest bg-white">Agent</div>
              <div className="bg-white border border-gray-200 shadow-sm text-gray-800 px-4 py-2.5 rounded-lg text-sm rounded-tl-sm w-full font-medium z-10">
                Main abhi aapko clinic se connect kar rahi hoon. Agar dard badh raha hai, turant nazdeeki emergency par jaiye.
              </div>
            </div>

            <div className="ml-[68px] mt-2 inline-block bg-red-50 text-red-700 text-[11px] font-bold px-3 py-1.5 rounded tracking-wide">
              Booking flow abandoned. No appointment was created.
            </div>
          </div>
        </div>

        {/* Outcome Area */}
        <div className="flex-1 bg-white rounded-lg border border-gray-200 p-6 shadow-sm flex flex-col h-fit">
          <h3 className="text-sm font-bold text-gray-800 mb-6">Outcome</h3>
          
          <table className="w-full text-sm">
            <tbody className="divide-y divide-gray-100 text-gray-500">
              <tr>
                <td className="py-3.5">terminal_state</td>
                <td className="py-3.5 text-right font-mono font-bold text-gray-800 text-[13px]">escalated</td>
              </tr>
              <tr>
                <td className="py-3.5">escalation_reason</td>
                <td className="py-3.5 text-right font-mono font-bold text-gray-800 text-[13px]">clinical_urgent</td>
              </tr>
              <tr>
                <td className="py-3.5">patient_id</td>
                <td className="py-3.5 text-right font-mono font-bold text-gray-800 text-[13px]">pt_0192</td>
              </tr>
              <tr>
                <td className="py-3.5">appointment_id</td>
                <td className="py-3.5 text-right font-mono font-bold text-gray-800 text-[13px]">null</td>
              </tr>
              <tr>
                <td className="py-3.5">tool_calls</td>
                <td className="py-3.5 text-right font-mono font-bold text-gray-800 text-[13px]">2</td>
              </tr>
              <tr>
                <td className="py-3.5">turns</td>
                <td className="py-3.5 text-right font-mono font-bold text-gray-800 text-[13px]">6</td>
              </tr>
              <tr>
                <td className="py-3.5">tokens</td>
                <td className="py-3.5 text-right font-mono font-bold text-gray-800 text-[13px]">3,140</td>
              </tr>
              <tr>
                <td className="py-3.5">latency</td>
                <td className="py-3.5 text-right font-mono font-bold text-gray-800 text-[13px]">4.2 s</td>
              </tr>
            </tbody>
          </table>

          <h3 className="text-[10px] font-bold text-gray-400 mt-10 mb-4 uppercase tracking-widest">Determinism</h3>
          <div className="flex justify-between items-center text-sm text-gray-500 bg-gray-50 p-3 rounded-lg border border-gray-100">
            <span className="font-medium text-[13px]">Same terminal state across 3 runs.</span>
            <span className="text-green-700 bg-green-50 border border-green-100 px-2 py-0.5 text-[10px] font-bold rounded tracking-wider">STABLE</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConversationDetail;
