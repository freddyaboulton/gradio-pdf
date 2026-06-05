<script lang="ts">
	import { tick } from "svelte";
	import PdfUploadText from "./PdfUploadText.svelte";
	import { Gradio } from "@gradio/utils";
	import type { SharedProps } from "@gradio/utils";
	import { Block, BlockLabel, Empty } from "@gradio/atoms";
	import { BaseButton } from "@gradio/button";
	import { File } from "@gradio/icons";
	import { StatusTracker } from "@gradio/statustracker";
	import type { FileData } from "@gradio/client";
	import { Upload, ModifyUpload } from "@gradio/upload";
	import * as pdfjsLib from "pdfjs-dist";

	interface PDFProps {
		value: FileData | null;
		height: number | null;
		starting_page: number;
	}

	interface PDFEvents {
		change: never;
		upload: never;
		clear_status: never;
		error: string;
	}

	let _props: { shared_props: SharedProps; props: PDFProps } = $props();
	const gradio = new Gradio<PDFEvents, PDFProps>(_props);

	pdfjsLib.GlobalWorkerOptions.workerSrc =
		"https://cdn.jsdelivr.net/gh/freddyaboulton/gradio-pdf@main/pdf.worker.min.mjs";

	let pdfDoc = $state<pdfjsLib.PDFDocumentProxy | null>(null);
	let numPages = $state(1);
	let canvasRef = $state<HTMLCanvasElement | null>(null);
	let currentPage = $state(1);
	let old_value = $state(gradio.props.value);
	let value_watcher_ready = false;
	let renderTask: pdfjsLib.RenderTask | null = null;

	let _value = $derived(gradio.props.value);

	$effect(() => {
		if (JSON.stringify(old_value) !== JSON.stringify(_value)) {
			if (_value) {
				get_doc(_value);
			} else {
				pdfDoc = null;
			}
			old_value = _value;
			if (value_watcher_ready) {
				gradio.dispatch("change");
			} else {
				value_watcher_ready = true;
			}
		}
	});

	function resolve_file_url(value: FileData): string {
		if (!value.url) {
			throw new Error("Uploaded file is missing a URL.");
		}
		if (value.url.startsWith("http://") || value.url.startsWith("https://")) {
			return value.url;
		}
		const backend_port = (window as any).__GRADIO__SERVER_PORT__;
		const root =
			gradio.shared.root ||
			(backend_port
				? `${window.location.protocol}//${window.location.hostname}:${backend_port}/`
				: window.location.origin + "/");
		return new URL(value.url, root).href;
	}

	async function handle_clear(): Promise<void> {
		gradio.props.value = null;
		pdfDoc = null;
		await tick();
		gradio.dispatch("change");
	}

	async function handle_upload(
		data: FileData | FileData[] | Blob | File
	): Promise<void> {
		const detail = Array.isArray(data) ? data[0] : (data as FileData);
		gradio.props.value = detail;
		await tick();
		gradio.dispatch("upload");
	}

	async function get_doc(value: FileData): Promise<void> {
		await tick();
		try {
			const url = resolve_file_url(value);
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
			numPages = pdfDoc.numPages;
			await tick();
			await go_to_page(
				Math.min(
					Math.max(gradio.props.starting_page ?? 1, 1),
					numPages
				)
			);
		} catch (error) {
			console.error("Failed to load PDF:", error);
			gradio.dispatch("error", String(error));
		}
	}

	async function render_page(pageNum: number): Promise<void> {
		if (!pdfDoc || !canvasRef) return;

		const pageIndex = Math.min(Math.max(Math.floor(pageNum), 1), numPages);
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

		const page = await doc.getPage(pageIndex);
		if (!canvasRef) return;
		const ctx = canvas.getContext("2d");
		if (!ctx) return;

		ctx.clearRect(0, 0, canvas.width, canvas.height);
		let viewport = page.getViewport({ scale: 1 });
		if (gradio.props.height) {
			viewport = page.getViewport({
				scale: gradio.props.height / viewport.height,
			});
		}
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

	async function go_to_page(pageNum: number): Promise<void> {
		if (!pdfDoc) return;
		currentPage = Math.min(Math.max(Math.floor(pageNum), 1), numPages);
		await render_page(currentPage);
	}

	function next_page(): void {
		if (currentPage >= numPages) return;
		void go_to_page(currentPage + 1);
	}

	function prev_page(): void {
		if (currentPage <= 1) return;
		void go_to_page(currentPage - 1);
	}

	function handle_page_change(): void {
		void go_to_page(currentPage);
	}

	function handle_page_keydown(event: KeyboardEvent): void {
		if (event.key === "Enter") {
			event.preventDefault();
			void go_to_page(currentPage);
		}
	}

	function num_digits(x: number): number {
		return (Math.log10((x ^ (x >> 31)) - (x >> 31)) | 0) + 1;
	}

	const client = gradio.shared.client;
</script>

<Block
	visible={gradio.shared.visible}
	elem_id={gradio.shared.elem_id}
	elem_classes={gradio.shared.elem_classes}
	container={gradio.shared.container}
	scale={gradio.shared.scale}
	min_width={gradio.shared.min_width}
>
	{#if gradio.shared.loading_status}
		<StatusTracker
			autoscroll={gradio.shared.autoscroll}
			i18n={gradio.i18n}
			{...gradio.shared.loading_status}
			show_validation_error={false}
			on_clear_status={() =>
				gradio.dispatch("clear_status", gradio.shared.loading_status)}
		/>
	{/if}
	<BlockLabel
		show_label={gradio.shared.label !== null}
		Icon={File}
		float={gradio.props.value === null}
		label={gradio.shared.label || "File"}
	/>
	{#if _value}
		<ModifyUpload i18n={gradio.i18n} onclear={handle_clear} />
		<div class="pdf-canvas">
			<canvas bind:this={canvasRef}></canvas>
		</div>
		<div class="button-row">
			<BaseButton
				elem_id={null}
				elem_classes={[]}
				visible={true}
				variant="secondary"
				size="sm"
				value={null}
				link={null}
				link_target="_self"
				icon={null}
				disabled={currentPage <= 1}
				scale={null}
				min_width={undefined}
				onclick={prev_page}
			>
				⬅️
			</BaseButton>
			<div class="page-count">
				<input
					type="number"
					style={`width: ${50 + num_digits(numPages) * 10}px`}
					bind:value={currentPage}
					onchange={handle_page_change}
					onkeydown={handle_page_keydown}
					min={1}
					max={numPages}
				/>
				<span style="padding: var(--size-1)"> / </span>
				<span style="padding-right: var(--size-2); width: fit-content">{numPages}</span>
			</div>
			<BaseButton
				elem_id={null}
				elem_classes={[]}
				visible={true}
				variant="secondary"
				size="sm"
				value={null}
				link={null}
				link_target="_self"
				icon={null}
				disabled={currentPage >= numPages}
				scale={null}
				min_width={undefined}
				onclick={next_page}
			>
				➡️
			</BaseButton>
		</div>
	{:else if gradio.shared.interactive}
		<Upload
			onload={handle_upload}
			onerror={(error) => {
				if (gradio.shared.loading_status) {
					gradio.shared.loading_status.status = "error";
				}
				gradio.dispatch("error", error);
			}}
			filetype=".pdf"
			file_count="single"
			show_progress={false}
			max_file_size={gradio.shared.max_file_size}
			root={gradio.shared.root}
			upload={client.upload.bind(client)}
			stream_handler={client.stream.bind(client)}
		>
			<PdfUploadText />
		</Upload>
	{:else}
		<Empty unpadded_box={true} size="large"><File /></Empty>
	{/if}
</Block>

<style>
	.pdf-canvas {
		display: flex;
		justify-content: center;
		align-items: center;
		overflow-y: auto;
	}

	.button-row {
		display: flex;
		flex-direction: row;
		width: 100%;
		justify-content: center;
		align-items: center;
	}

	.page-count {
		font-family: var(--font-mono);
		display: flex;
		flex-direction: row;
		justify-content: space-evenly !important;
		align-items: center;
	}

	input[type="number"] {
		outline: none !important;
		border: none;
		background: var(--input-background-fill);
		color: var(--body-text-color);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		text-align: center;
	}

	input:disabled {
		-webkit-text-fill-color: var(--body-text-color);
		-webkit-opacity: 1;
		opacity: 1;
	}

	input[type="number"]:focus {
		box-shadow: var(--input-shadow-focus);
		border-color: var(--input-border-color-focus);
	}

	input::placeholder {
		color: var(--input-placeholder-color);
	}
</style>
