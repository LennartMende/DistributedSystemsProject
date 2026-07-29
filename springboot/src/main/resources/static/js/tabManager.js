export class TabManager {
    constructor(pageName) {
        this.pageName = pageName;
        this.id = crypto.randomUUID();
        this.channel = new BroadcastChannel("robot-dashboard");
        this.tabs = new Map();

        this.tabs.set(this.id, {
            page: this.pageName,
            lastSeen: Date.now()
        });

        this.lastMode = null;

        this.channel.onmessage =
            this.onMessage.bind(this);
        window.addEventListener(
            "beforeunload",
            this.onClose.bind(this)
        );

        setInterval(() => {
            this.sendHeartbeat();
        }, 1000);
        setInterval(() => {
            this.removeDeadTabs();
        }, 1000);
        setInterval(() => {
            this.updateRest();
        }, 1000);
    }

    start() { // sending a hello when the tab is opened
        this.channel.postMessage({
            type: "hello",
            id: this.id,
            page: this.pageName
        });

        this.sendHeartbeat();
    }

    onMessage(event) {
        const msg = event.data;
        if (msg.type === "hello") {
            if (msg.id === this.id) {
                return;
            }

            this.tabs.set(msg.id, {
                page: msg.page,
                lastSeen: Date.now()
            });

            this.channel.postMessage({
                type: "iam",
                id: this.id,
                page: this.pageName
            });
        }

        if (msg.type === "iam") {
            this.tabs.set(msg.id, {
                page: msg.page,
                lastSeen: Date.now()
            });
        }

        if (msg.type === "closed") {
            this.tabs.delete(msg.id);
        }

        if (msg.type === "alive") {
            const tab = this.tabs.get(msg.id);
            if (tab) {
                tab.lastSeen = Date.now();
            }
        }
    }

    onClose() {
        this.channel.postMessage({
            type: "closed",
            id: this.id,
            page: this.pageName
        });
    }

    getPageCounter() {
        const counter = {
            index: 0,
            diagram: 0,
            control: 0
        };

        console.log(this.tabs);
        console.log([...this.tabs.entries()]);

        for (const tab of this.tabs.values()) {
            counter[tab.page]++;
        }
        return counter;
    }

    takeControl() {
        return (this.getPageCounter().control > 0);
    }

    justObserve() {
        return ((this.getPageCounter().index + this.getPageCounter().diagram) > 0);
    }

    hasConflict() {
        const count = this.getPageCounter();
        return (((count.index + count.diagram) > 0 && count.control > 0) // observe + control
            || 
            (count.control > 1)); // multiple control
    }

    sendHeartbeat() {
        this.channel.postMessage({
            type: "alive",
            id: this.id
        });
    }

    removeDeadTabs() {
        const ownTab = this.tabs.get(this.id);

        if (ownTab) {
            ownTab.lastSeen = Date.now();
        }

        this.channel.postMessage({
            type: "alive",
            id: this.id
        });
    }


    getMode() {
        if (this.hasConflict()) {
            return "conflict";
        }
        if (this.takeControl()) {
            return "control";
        }
        return "observe";
    }


    async updateRest() {
        const mode = this.getMode();
        if(mode === this.lastMode){ // mode didn't change
            return;
        }

        this.lastMode = mode; // mode did change
        await fetch("/api/dashboard/mode", {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                "time": Date.now() / 1000,
                "deviceId": "dashboard_mode_publisher",
                mode: mode
            })
        });
    }

}
