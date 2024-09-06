	<script lang="ts">
		import { tick } from "svelte";
		import PdfUploadText from "./PdfUploadText.svelte";
		import type { Gradio } from "@gradio/utils";
		import { Block, BlockLabel } from "@gradio/atoms";
		import { BaseButton } from "@gradio/button";
		import { File } from "@gradio/icons";
		import { StatusTracker } from "@gradio/statustracker";
		import type { LoadingStatus } from "@gradio/statustracker";
		import type { FileData } from "@gradio/client";
		import { Upload, ModifyUpload } from "@gradio/upload";
		import * as pdfjsLib from 'pdfjs-dist';

		export let elem_id = "";
		export let elem_classes: string[] = [];
		export let visible = true;
		export let value: FileData | null = null;
		export let container = true;
		export let scale: number | null = null;
		export let root: string;
		export let height: number | null = null;
        export let starting_page: number;
		export let label: string;
		export let proxy_url: string;
		export let min_width: number | undefined = undefined;
		export let loading_status: LoadingStatus;
		export let gradio: Gradio<{
			change: never;
			upload: never;
			clear_status: never;
		}>;

		pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdn.jsdelivr.net/gh/freddyaboulton/gradio-pdf@main/pdf.worker.min.mjs";
		
		let _value;
		let old_value;
		let pdfDoc;
		let numPages = 1;
		let canvasRef;

		$: currentPage = Math.min(Math.max(starting_page, 1), numPages);

		async function handle_clear() {
			_value = null;
			await tick();
			gradio.dispatch("change");
		}

		async function handle_upload({detail}: CustomEvent<FileData>): Promise<void> {
			value = detail;
			await tick();
			gradio.dispatch("change");
			gradio.dispatch("upload");
		}


		async function get_doc(value: FileData) {
			const loadingTask = pdfjsLib.getDocument(value.url);
			pdfDoc = await loadingTask.promise;
			numPages = pdfDoc.numPages;
			currentPage = Math.min(Math.max(starting_page, 1), numPages)
			render_page(currentPage);
		}

		function render_page(currentPage) {
		// Render a specific page of the PDF onto the canvas
			pdfDoc.getPage(currentPage).then(page => {
				const ctx  = canvasRef.getContext('2d')
				ctx.clearRect(0, 0, canvasRef.width, canvasRef.height);
				let viewport = page.getViewport({ scale: 1 });
				console.log("height", height)
				if (height) {
					viewport = page.getViewport({ scale: height / viewport.height });
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
			render_page(currentPage);
		}

		function prev_page() {
			if (currentPage == 1) {
				return;
			}
			currentPage--;
			render_page(currentPage);
		}

		function handle_page_change() {
			if(currentPage < 1) return;
			if(currentPage > numPages) return;
			render_page(currentPage)
		}

		function num_digits(x) {
  			return (Math.log10((x ^ (x >> 31)) - (x >> 31)) | 0) + 1;
		}

		function normalise_file(value, root, proxy_url) {
			return value
		}
		
		// Compute the url to fetch the file from the backend\
		// whenever a new value is passed in.
		$: _value = normalise_file(value, root, proxy_url);

		// If the value changes, render the PDF of the currentPage
		$: if(JSON.stringify(old_value) != JSON.stringify(_value)) {
			if (_value){
				get_doc(_value);
			}
			old_value = _value;
			gradio.dispatch("change");
		}
	</script>

	<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
		{#if loading_status}
			<StatusTracker
				autoscroll={gradio.autoscroll}
				i18n={gradio.i18n}
				{...loading_status}
				on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
			/>
		{/if}
		<BlockLabel
			show_label={label !== null}
			Icon={File}
			float={value === null}
			label={label || "File"}
		/>
		{#if _value}
			<ModifyUpload i18n={gradio.i18n} on:clear={handle_clear} absolute />
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
		{:else}
			<Upload
				on:load={handle_upload}
				on:error={({ detail }) => {
					loading_status = loading_status || {};
					loading_status.status = "error";
					gradio.dispatch("error", detail);
				}}
				filetype={".pdf"}
				file_count="single"
				{root}
				max_file_size={gradio.max_file_size}
				upload={gradio.client.upload}
				stream_handler={gradio.client.stream}
			>
				<PdfUploadText/>
			</Upload>
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