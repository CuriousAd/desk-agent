import { useState } from 'react'
import HandoffQueue from './components/HandoffQueue'
import ConversationDetail from './components/ConversationDetail'

function App() {
  const [activeTab, setActiveTab] = useState(0)

  return (
    <div className="min-h-screen bg-white">
      <header className="flex justify-between items-center p-6 border-b border-gray-200">
        <div className="text-sm font-semibold text-blue-900 leading-tight">
          CIN - U63999UT2025PTC020308<br/>
          20 Dav College Road, Karanpur,<br/>
          Dehradun - 248001, Uttarakhand, India
        </div>
        <div className="text-4xl font-bold text-blue-900 flex items-center tracking-tight">
          Swasthiq<span className="text-teal-400 ml-0.5 mt-1 text-5xl">+</span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto mt-12 mb-12">
        <h1 className="text-2xl font-bold text-blue-900 mb-6">
          {activeTab === 0 ? "1. Handoff Queue" : "2. Conversation Detail"}
        </h1>
        
        <div className="flex bg-white rounded-lg border border-gray-200 overflow-hidden min-h-[600px] shadow-sm">
          {/* Sidebar */}
          <div className="w-16 bg-gray-50 border-r border-gray-200 flex flex-col items-center py-6 gap-6 pt-10">
            {[0, 1, 2, 3, 4, 5, 6].map((i) => (
              <button 
                key={i} 
                onClick={() => setActiveTab(i === 0 ? 0 : 1)}
                className={`w-3.5 h-3.5 rounded-full border-2 transition-all duration-200 ${
                  (activeTab === 0 && i === 0) || (activeTab === 1 && i === 2)
                    ? 'border-blue-500 ring-2 ring-blue-100 bg-white' 
                    : 'border-gray-300 bg-transparent hover:border-gray-400'
                }`}
              />
            ))}
          </div>

          {/* Content */}
          <div className="flex-1 bg-gray-50 p-10">
             {activeTab === 0 ? <HandoffQueue /> : <ConversationDetail />}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
