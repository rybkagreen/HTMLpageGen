import Image from 'next/image';
import Link from 'next/link';

export default function Navbar() {
  return (
    <header className='sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60'>
      <div className='container flex h-16 items-center'>
        <div className='mr-4 flex'>
          <Link href='/' className='flex items-center space-x-2'>
            <Image src='/file.svg' alt='Logo' width={24} height={24} />
            <span className='font-bold'>HTMLpageGen</span>
          </Link>
        </div>
        <nav className='flex flex-1 items-center justify-between space-x-2 md:justify-end'>
          <div className='flex items-center gap-5'>
            <Link
              href='/'
              className='text-sm font-medium transition-colors hover:text-primary'
            >
              Главная
            </Link>
            <Link
              href='/generator'
              className='text-sm font-medium transition-colors hover:text-primary'
            >
              Генератор
            </Link>
            <Link
              href='/projects'
              className='text-sm font-medium transition-colors hover:text-primary'
            >
              Проекты
            </Link>
            <Link
              href='/chat'
              className='text-sm font-medium transition-colors hover:text-primary'
            >
              ИИ Чат
            </Link>
            <Link
              href='/templates'
              className='text-sm font-medium transition-colors hover:text-primary'
            >
              Шаблоны
            </Link>
            <Link
              href='/docs'
              className='text-sm font-medium transition-colors hover:text-primary'
            >
              Документация
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
}
