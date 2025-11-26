<script lang="ts">
	import { tick } from "svelte";
	import PdfUploadText from "./PdfUploadText.svelte";
	import { Gradio } from "@gradio/utils";
	import { Block, BlockLabel, Empty} from "@gradio/atoms";
	import { BaseButton } from "@gradio/button";
	import { File } from "@gradio/icons";
	import { StatusTracker } from "@gradio/statustracker";
	import type { FileData } from "@gradio/client";
	import { Upload, ModifyUpload } from "@gradio/upload";
	import * as pdfjsLib from 'pdfjs-dist';

	const _props = $props();
	const gradio = new Gradio(_props);

	pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdn.jsdelivr.net/gh/freddyaboulton/gradio-pdf@main/pdf.worker.min.mjs";

	let old_value = $state(gradio.props.value);
	let pdfDoc;
	let numPages = $state(1);
	let canvasRef;

	let currentPage = $derived(Math.min(Math.max(gradio.props.starting_page, 1), numPages))


	$effect(() => render_page(currentPage));

	async function handle_clear() {
		gradio.props.value = null;
		await tick();
		gradio.dispatch("change");
	}

	async function handle_upload({detail}: CustomEvent<FileData>): Promise<void> {
		gradio.props.value = detail;
		await tick();
		gradio.dispatch("upload");
	}


	async function get_doc(value: FileData) {
		const loadingTask = pdfjsLib.getDocument({
			url: value.url,
			cMapUrl: "https://huggingface.co/datasets/freddyaboulton/bucket/resolve/main/cmaps/",
			cMapPacked: true,
		});
		pdfDoc = await loadingTask.promise;
		numPages = pdfDoc.numPages;
		currentPage = Math.min(Math.max(gradio.props.starting_page, 1), numPages)
		render_page(currentPage);
	}

	function render_page(currentPage) {
		if(!pdfDoc) return;
		// Render a specific page of the PDF onto the canvas
		pdfDoc.getPage(currentPage).then(page => {
			const ctx  = canvasRef.getContext('2d')
			ctx.clearRect(0, 0, canvasRef.width, canvasRef.height);
			let viewport = page.getViewport({ scale: 1 });
			if (gradio.props.height) {
				viewport = page.getViewport({ scale: gradio.props.height / viewport.height });
			}
			const renderContext = {
				canvasContext: ctx,
				viewport,
			};
			canvasRef.width = viewport.width;
			canvasRef.height = viewport.height;
			page.render(renderContext);
		});
	}

	function next_page() {
		if (currentPage >= numPages) {
			return;
		}
		currentPage++;
	}

	function prev_page() {
		if (currentPage == 1) {
			return;
		}
		currentPage--;
	}

	function handle_page_change() {
		if(currentPage < 1) return;
		if(currentPage > numPages) return;
	}

	function num_digits(x) {
		return (Math.log10((x ^ (x >> 31)) - (x >> 31)) | 0) + 1;
	}

	// Compute the url to fetch the file from the backend\
	// whenever a new value is passed in.
	let _value = $derived(gradio.props.value);

	// If the value changes, render the PDF of the currentPage
	$effect(() => {
	if(JSON.stringify(old_value) != JSON.stringify(_value)) {
		if (_value){
			get_doc(_value);
		}
		old_value = _value;
		gradio.dispatch("change");
	}
	});
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
		<ModifyUpload i18n={gradio.i18n} on:clear={handle_clear} />
		<div class="pdf-canvas">
			<canvas bind:this={canvasRef}></canvas>
		</div>
		<div class="button-row">
			<BaseButton on:click={prev_page}>
				⬅️
			</BaseButton>
			<div class="page-count">
				<input type="number" style={`width: ${50 + num_digits(numPages) * 10}px`} bind:value={currentPage} on:change={handle_page_change} min={1} max={numPages}  />
				<span style="padding: var(--size-1)"> / </span> 
				<span style="padding-right: var(--size-2); width: fit-content">{numPages}</span>
			</div>
			<BaseButton on:click={next_page}>
				➡️
			</BaseButton>
		</div>
	{:else if gradio.shared.interactive}
		<Upload
			on:load={handle_upload}
			on:error={({ detail }) => {
				loading_status = loading_status || {};
				loading_status.status = "error";
				gradio.dispatch("error", detail);
			}}
			filetype={".pdf"}
			file_count="single"
			max_file_size={gradio.shared.max_file_size}
			upload={(...args) => gradio.shared.client.upload(...args)}
			stream_handler={gradio.shared.client?.stream}
			root={gradio.shared.root}
		>
			<PdfUploadText/>
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