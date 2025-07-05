export default function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="border-t py-6 md:py-0">
      <div className="container flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row">
        <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
          © {currentYear} HTMLpageGen. Все права защищены.
        </p>
        <div className="flex items-center gap-4">
          <a 
            href="https://github.com/yourusername/HTMLpageGen" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            GitHub
          </a>
          <a 
            href="/docs" 
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            Документация
          </a>
          <a 
            href="/privacy" 
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            Политика конфиденциальности
          </a>
        </div>
      </div>
    </footer>
  );
}
