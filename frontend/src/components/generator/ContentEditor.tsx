
interface ContentEditorProps {
  content: string;
  onChange: (content: string) => void;
}

export default function ContentEditor({ content, onChange }: ContentEditorProps) {
  return (
    <div className="flex flex-col space-y-2">
      <label htmlFor="content" className="text-sm font-medium">
        Контент для генерации HTML
      </label>
      <textarea
        id="content"
        className="min-h-[300px] w-full resize-y rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        placeholder="Введите текстовое описание контента..."
        value={content}
        onChange={(e) => onChange(e.target.value)}
      />
      <p className="text-xs text-muted-foreground">
        Длина: {content.length} символов | Слов: {content.split(/\s+/).filter(Boolean).length}
      </p>
    </div>
  );
}
