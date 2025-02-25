"use client"; 

import Link from 'next/link';
import { UserCircleIcon, HomeIcon } from '@heroicons/react/24/outline';
import Sidebar from '@/app/ui/chatbox/sidebar'; 
import { usePathname } from 'next/navigation'; 
import clsx from 'clsx';  

export default function SideNav() { 
  const pathname = usePathname(); 

  return (
    <div className="flex w-[250px] h-full bg-blue-100  flex-col px-3 md:px-2"> 
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
      <div><Sidebar/></div> 
      <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
      </div>
    </div>
  );
} 
