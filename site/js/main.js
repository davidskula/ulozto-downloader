ready(() => {
    let vm = {
        dwUrl: ko.observable(),
        dwDir: ko.observable(),
        dwParts: ko.observable(15),
        startDownload: async () => {
            const data = {
                url: vm.dwUrl(),
                out: vm.dwDir(),
                parts: vm.dwParts()
            };
            let ret = await fetch("/queue", {
                method: "POST",
                body: JSON.stringify(data),
                headers: { "Content-type": "application/json" }
            });
        },
        
        actDwActive: ko.observable(true),
        actDw: ko.observable(),
        showActDw: () =>{
            vm.queueActive(false);
            vm.historyActive(false);
            vm.actDwActive(true);
        },

        queueActive: ko.observable(false),
        queue: ko.observable(),
        showQueue: () =>{
            vm.queueActive(true);
            vm.historyActive(false);
            vm.actDwActive(false);
        },

        
        historyActive: ko.observable(false),
        history: ko.observable(),
        showHistory: () =>{
            vm.queueActive(false);
            vm.historyActive(true);
            vm.actDwActive(false);
        },
    }

    // vm.queue([
    //     {
    //         url: "dadd",
    //         out: "ddd",
    //         parts: 12
    //     },{
    //         url: "dadd",
    //         out: "ddd",
    //         parts: 12
    //     },{
    //         url: "dadd",
    //         out: "ddd",
    //         parts: 12
    //     },{
    //         url: "dadd",
    //         out: "ddd",
    //         parts: 12
    //     }
    // ]);

    // vm.actDw({
    //     url: "aaa",
    //     out: "dir",
    //     file: "file",
    //     type: "type",
    //     size: 123,
    //     parts: [
    //         "aaaa", "bbbb", "cccc"
    //     ],
    //     logs: [
    //         "ddddd", "eeee"
    //     ]
    // });

    ko.applyBindings(vm);

    setInterval(async () => {
        let ret = await fetch("/actDownloading");
        let data = await ret.json();
        vm.actDw(data);
    }, 500);

    setInterval(async () => {
        let ret = await fetch("/queue");
        let data = await ret.json();
        vm.queue(data);

        ret = await fetch("/history");
        data = await ret.json();
        vm.history(data);
    }, 1000);
})