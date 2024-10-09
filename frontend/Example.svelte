<script lang="ts">
	export let value: object;
	export let samples_dir: string;
	export let type: "gallery" | "table";
	export let selected = false;
	import * as pdfjsLib from 'pdfjs-dist';
	pdfjsLib.GlobalWorkerOptions.workerSrc =  "https://cdn.jsdelivr.net/gh/freddyaboulton/gradio-pdf@main/pdf.worker.min.mjs";
	
	let pdfDoc;
	let canvasRef;

	async function get_doc(url: string) {
		const loadingTask = pdfjsLib.getDocument(url);
		pdfDoc = await loadingTask.promise;
		renderPage();
		}

	function renderPage() {
		// Render a specific page of the PDF onto the canvas
			pdfDoc.getPage(1).then(page => {
				const ctx  = canvasRef.getContext('2d')
				ctx.clearRect(0, 0, canvasRef.width, canvasRef.height);
				
				const viewport = page.getViewport({ scale: 0.2 });
				
				const renderContext = {
					canvasContext: ctx,
					viewport
				};
				canvasRef.width = viewport.width;
				canvasRef.height = viewport.height;
				page.render(renderContext);
			});
		}
	
	$: get_doc(value.url);
</script>

<div
	class:table={type === "table"}
	class:gallery={type === "gallery"}
	class:selected
	style="justify-content: center; align-items: center; display: flex; flex-direction: column;"
>
	<canvas bind:this={canvasRef}></canvas>
</div>

<style>
	.gallery {
		padding: var(--size-1) var(--size-2);
	}
</style>
