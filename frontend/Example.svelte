<script lang="ts">
	import { tick } from "svelte";
	import type { FileData } from "@gradio/client";
	import * as pdfjsLib from "pdfjs-dist";

	let {
		value,
		type,
		selected = false,
		root = "",
	}: {
		value: FileData;
		type: "gallery" | "table";
		selected?: boolean;
		root?: string;
	} = $props();

	pdfjsLib.GlobalWorkerOptions.workerSrc =
		"https://cdn.jsdelivr.net/gh/freddyaboulton/gradio-pdf@main/pdf.worker.min.mjs";

	let pdfDoc = $state<pdfjsLib.PDFDocumentProxy | null>(null);
	let canvasRef = $state<HTMLCanvasElement | null>(null);
	let renderTask: pdfjsLib.RenderTask | null = null;

	function resolve_file_url(file: FileData): string {
		if (file.url) {
			if (file.url.startsWith("http://") || file.url.startsWith("https://")) {
				return file.url;
			}
			const backend_port = (window as any).__GRADIO__SERVER_PORT__;
			const base =
				root ||
				(backend_port
					? `${window.location.protocol}//${window.location.hostname}:${backend_port}/`
					: window.location.origin + "/");
			return new URL(file.url, base).href;
		}
		if (file.path) {
			const backend_port = (window as any).__GRADIO__SERVER_PORT__;
			const base =
				root ||
				(backend_port
					? `${window.location.protocol}//${window.location.hostname}:${backend_port}/`
					: window.location.origin + "/");
			return new URL(`/file=${file.path}`, base).href;
		}
		throw new Error("Example file is missing url or path");
	}

	async function load_pdf(file: FileData): Promise<void> {
		await tick();
		try {
			const url = resolve_file_url(file);
			const response = await fetch(url, { credentials: "include" });
			if (!response.ok) {
				throw new Error(`Failed to fetch PDF (${response.status})`);
			}
			const data = await response.arrayBuffer();
			const loadingTask = pdfjsLib.getDocument({
				data,
				cMapUrl:
					"https://huggingface.co/datasets/freddyaboulton/bucket/resolve/main/cmaps/",
				cMapPacked: true,
			});
			pdfDoc = await loadingTask.promise;
			await tick();
			await render_page();
		} catch (error) {
			console.error("Failed to load example PDF:", error);
			pdfDoc = null;
		}
	}

	async function render_page(): Promise<void> {
		if (!pdfDoc || !canvasRef) return;

		const doc = pdfDoc;
		const canvas = canvasRef;

		if (renderTask) {
			try {
				renderTask.cancel();
			} catch {
				// ignore cancelled render
			}
			renderTask = null;
		}

		const page = await doc.getPage(1);
		if (!canvasRef) return;
		const ctx = canvas.getContext("2d");
		if (!ctx) return;

		ctx.clearRect(0, 0, canvas.width, canvas.height);
		const viewport = page.getViewport({ scale: 0.2 });
		canvas.width = viewport.width;
		canvas.height = viewport.height;
		renderTask = page.render({ canvasContext: ctx, viewport });
		try {
			await renderTask.promise;
		} catch (error) {
			if ((error as { name?: string }).name === "RenderingCancelledException") {
				return;
			}
			throw error;
		} finally {
			renderTask = null;
		}
	}

	$effect(() => {
		if (value?.url || value?.path) {
			void load_pdf(value);
		} else {
			pdfDoc = null;
		}
	});
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
