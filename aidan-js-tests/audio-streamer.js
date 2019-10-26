class AudioStreamer extends AudioWorkletProcessor {
    constructor() {
        super();

        this.bufferSize = 128;
        this.buffer = new Float32Array(this.bufferSize * 128);
        this.bufferCount = 0;

        this.index = 0;
    }

    process (inputs, outputs, parameters) {

        for(let i = 0; i < 128; i++) {
            this.buffer[i + this.bufferCount * this.bufferSize] = inputs[0][0][i];
        }

        this.bufferCount ++;

        if(this.bufferCount >= this.bufferSize) {
            console.log("buffer count creater");
            console.log(this.buffer);

            // call felix function
            this.ondataavailable(this.buffer);

            // reset
            this.buffer = new Float32Array(this.bufferSize * 128);
            this.bufferCount = 0;
        }

        return true;
    }

    async ondataavailable(data) {

        console.log("hey");

        // felix: The binary data is somewhere in here. I can help with this.
        //console.log(event);

        const packet = {"data" : data, "index" : this.index++};

        console.log(packet);

        const xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST", "http://35.193.212.185/api/stream/1", true);
        xmlHttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xmlHttp.send(JSON.stringify(packet));

        xmlHttp.addEventListener("load", this.serverCallback, false);
    };

    serverCallback(data) {
        console.log(data);
    }
}

let packetIndex = 0;


registerProcessor('audio-streamer', AudioStreamer);