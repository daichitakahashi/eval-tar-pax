import { createTarPacker, createTarDecoder, type TarPackController } from 'modern-tar';

const dataSize = 1024 * 1024 //1MB // * 1024; // 1GB

const createTarStream = async (ctl: TarPackController) => {
	const targets = ["a", "b", "c", "d", "e"];
	
	for (const target of targets) {
		console.log("target:", target);
		const stream = ctl.add({
			name: target,
			size: dataSize,
			type: "file",
			pax: {
				"customHeader": target
			},
		})
		const w = stream.getWriter()
		for (let i = 0; i < 1024; i++) {
			await w.write(new Uint8Array(dataSize / 1024).fill(target.charCodeAt(0)));
		}
		// await w.write(new Uint8Array(dataSize).fill(1));
		// 1KBのデータを書き込む
		// await w.write(new Uint8Array(1024).fill(1));
		await w.close()
	}
	ctl.finalize()
}

export default {
	async fetch(request, env, ctx): Promise<Response> {
		const url = new URL(request.url);
		if (url.pathname !== "/") {
			return new Response("Not Found", { status: 404 });
		}
		// send
		const { readable, controller } = createTarPacker()
		// await createTarStream(controller)
		const [, resp] = await Promise.all([
			// Promise.resolve(),
			createTarStream(controller),
			fetch("http://localhost:8080", {
				method: 'POST',
				headers: {
					"Content-Type": "application/x-tar",
				},
				body: readable,
			})
		])

		// receive
		console.log("Returned entries:")
		const stream = resp.body!.pipeThrough(createTarDecoder({ strict: true }))
		for await(const entry of stream) {
			console.log(`Entry: ${entry.header.name}, Type: ${entry.header.type}, Size: ${entry.header.size}`);
			console.log(`PAX header: ${JSON.stringify(entry.header.pax)}`)
			console.log()
			await entry.body.cancel() // we don't need the body
		}
		
		return new Response("OK");
	},
} satisfies ExportedHandler<Env>;
