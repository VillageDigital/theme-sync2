export default function DashboardCard() {
    return (
      <div className="p-6 min-h-screen bg-gradient-to-br from-white via-slate-100 to-gray-200">
        <div className="max-w-md mx-auto bg-white shadow-xl rounded-2xl overflow-hidden">
          <div className="p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              🎯 Welcome to ThemeSync2
            </h2>
            <p className="text-gray-600 text-sm mb-4">
              This is a sample dashboard card styled with TailwindCSS. You’re all set to start building your smart, snazzy UI.
            </p>
  
            <div className="flex space-x-4">
              <button className="px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-xl shadow hover:bg-indigo-700 transition duration-300">
                Run Theme Sync
              </button>
              <button className="px-4 py-2 border border-gray-300 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-100 transition duration-300">
                Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
  