
"use client"; 

import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import styles from '@/app/ui/home.module.css';
import { lusitana } from '@/app/ui/fonts';
import Image from 'next/image'; 
import { usePathname } from 'next/navigation'; 
import clsx from 'clsx';  

export default function Page() { 
  const pathname = usePathname(); 

  return (
    <main className="flex min-h-screen flex-col p-6"> 
     <p>Home Page</p> 
     <div>
     <Link
            href='/chatbox'
            className={clsx(
              'flex h-[48px] items-center justify-center gap-2 rounded-md p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3',
              {
                'bg-sky-100 text-blue-600': pathname === '/chatbox', 
              },
            )}
          > 
          <ArrowRightIcon className="w-10" />
      </Link>
      </div>
    </main>
  );
}
