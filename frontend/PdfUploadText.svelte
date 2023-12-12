<script lang="ts">
	import { Upload as UploadIcon } from "@gradio/icons";
	export let hovered = false;

</script>

<div class="wrap">
	<span class="icon-wrap" class:hovered><UploadIcon /> </span>
    Drop PDF
    <span class="or">- or -</span>
    Click to Upload

</div>

<style>
	.wrap {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		min-height: var(--size-60);
		color: var(--block-label-text-color);
		line-height: var(--line-md);
		height: 100%;
		padding-top: var(--size-3);
	}

	.or {
		color: var(--body-text-color-subdued);
		display: flex;
	}

	.icon-wrap {
		width: 30px;
		margin-bottom: var(--spacing-lg);
	}

	@media (--screen-md) {
		.wrap {
			font-size: var(--text-lg);
		}
	}

	.hovered {
		color: var(--color-accent);
	}
</style>
