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
		export let height: number | null = 500;
        export let starting_page: number;
		export let label: string;
		export let proxy_url: string;
		export let min_width: number | undefined = undefined;
		export let loading_status: LoadingStatus;
		export let gradio: Gradio<{
			change: never;
			upload: never;
		}>;


		pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdn.jsdelivr.net/gh/freddyaboulton/gradio-pdf@main/pdf.worker.min.mjs";
		
		let _value = value;
		let old_value = _value;
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
				let scale = height / viewport.height;
				viewport = page.getViewport({ scale: scale });

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

		$: height = height || 500;

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
			<div class="pdf-canvas" style="height: {height}px">
				<canvas bind:this={canvasRef}></canvas>
			</div>
			<div class="button-row">
				<BaseButton on:click={prev_page}>
					⬅️
				</BaseButton>
				<span class="page-count"> {currentPage} / {numPages} </span>
				<BaseButton on:click={next_page}>
					➡️
				</BaseButton>
			</div>
		{:else}
			<Upload
				on:load={handle_upload}
				filetype={"application/pdf"}
				file_count="single"
				{root}
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
		margin: 0 10px;
		font-family: var(--font-mono);
	}

</style>