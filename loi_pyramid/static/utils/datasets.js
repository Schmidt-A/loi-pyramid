export class Dataset {
    constructor(name, retrieve) {
        this.name = name;
        this.retrieve = retrieve;
    }

    getData(parentData) {
        let data = sessionStorage.getItem(`${this.name}`);
        if (!data) {
                return this.retrieve(parentData).then( data => {
                    sessionStorage.setItem(`${this.name}`, JSON.stringify(data));
                    return data; 
                })
        } else {
            return new Promise((resolve, reject) => { 
                resolve(JSON.parse(data))
            })
        }
    }
}