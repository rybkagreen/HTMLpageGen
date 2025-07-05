import { useEffect, useRef } from "react";

interface HTMLPreviewProps {
  html: string;
}

export default function HTMLPreview({ html }: HTMLPreviewProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    if (iframeRef.current && html) {
      const iframe = iframeRef.current;
      const doc = iframe.contentDocument;
      if (doc) {
        doc.open();
        doc.write(html);
        doc.close();
      }
    }
  }, [html]);

  return (
    <div className="flex flex-col space-y-2">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium">Предпросмотр HTML</h3>
        {html && (
          <button
            className="text-xs text-blue-600 hover:underline"
            onClick={() => {
              const blob = new Blob([html], { type: "text/html" });
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = "generated-page.html";
              a.click();
              URL.revokeObjectURL(url);
            }}
          >
            Скачать HTML
          </button>
        )}
      </div>
      {html ? (
        <div className="overflow-hidden rounded-md border border-input">
          <iframe
            ref={iframeRef}
            title="HTML Preview"
            className="h-[500px] w-full"
          />
        </div>
      ) : (
        <div className="flex h-[500px] items-center justify-center rounded-md border border-dashed border-input">
          <p className="text-sm text-muted-foreground">
            Здесь будет отображаться предпросмотр сгенерированной страницы
          </p>
        </div>
      )}
    </div>
  );
}
