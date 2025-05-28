export default {
  async fetch(request) {
    const url = new URL(request.url);

    // Replace this with your actual backend/proxy target
    const targetHost = "https://aidne-production-7a97.up.railway.app";

    // Rewrite request to target
    url.hostname = targetHost.replace("https://", "").replace("http://", "");

    const proxyRequest = new Request(url.toString(), request);
    const response = await fetch(proxyRequest);

    return response;
  },
};
