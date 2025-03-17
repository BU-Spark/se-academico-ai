import { UserCircleIcon, HomeIcon, PlusIcon, PencilSquareIcon} from '@heroicons/react/24/outline';
import { usePathname } from 'next/navigation'; 
import clsx from 'clsx';  
import Link from 'next/link'; 

export default function ChatHistory({ sessions, selectChat }) {
  const pathname = usePathname(); 

  return (
    <div className="w-96 p-4 border-r bg-blue-100 h-screen">
      {/* User Profile */}
      <div className="mb-2 flex h-20 items-center justify-start rounded-md bg-blue-400 p-4 md:h-[100px]">
        <div className="w-full text-white items-center space-x-5 md:w-full flex">
          {/* Container for UserCircleIcon and text */}
          <div className="flex items-center space-x-2">
            <UserCircleIcon className="w-10 h-10" />
            <h1 className="text-lg whitespace-nowrap">Academic Amy</h1>
          </div>

          {/* Home Link */}
          <Link
            href='/'
            className={clsx(
              'flex h-[48px] items-center justify-center gap-2 rounded-md p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3',
              {
                'bg-sky-100 text-blue-600': pathname === '/',
              },
            )}
          >
            <HomeIcon className="w-8" />
          </Link>
        </div>
      </div>
      <div className = "h-5"></div> 

      {/* Add New Button*/}
      <div className="px-4 flex space-x-2">
        <button 
          onClick={() => window.location.reload()} 
          className="bg-blue-500 text-white px-3 py-1 flex items-center space-x-2 gap-1 rounded hover:bg-sky-100 hover:text-blue-600">
          New <PencilSquareIcon className="w-6"/>
        </button>
      </div> 
      <div className = "h-3"></div> 

      {/* Chat History */}
      <h2 className="text-lg font-bold px-2">Chat History</h2> 
      <div className="max-h-[70vh] overflow-y-auto p-2">
      {sessions.length === 0 && <p className="text-gray-500">No chat history so far </p>}
      <ul>
        {sessions.map((session) => (
          <li
            key={session.id}
            className="cursor-pointer p-2 bg-blue-400 text-white hover:bg-sky-100 hover:text-blue-600 my-2 rounded hover:bg-blue-200"
            onClick={() => selectChat(session.id)}
          >
            {session.title}
          </li>
        ))}
      </ul> 
      </div>

      {/* Add New Chat Plus Button */}
      <div className="p-4 flex justify-center">
        <button 
          onClick={() => window.location.reload()}
          className="text-white text-2xl bg-gray-300 p-1 rounded"
        >
        <PlusIcon className="w-3 h-3 text-black" />
      </button>
      </div>
    </div>
  );
}