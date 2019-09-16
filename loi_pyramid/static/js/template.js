class Content {
	constructor(id, beforeRender, markup, afterRender) {
		this.id = id;
		this.beforeRender = beforeRender;
		this.markup = markup;
		this.afterRender = afterRender;
	}

	render(parent) {
		if (parent && parent.children.length > 0) {
			parent.removeChild(parent.children[0])
		}

		let container = document.createElement("div");
		container.id = this.id;
	    container.innerHTML = this.markup;

	    parent.appendChild(container);
	}
}

class Page extends Content {
	constructor(id, beforeRender, markup, afterRender) {
		super(id, beforeRender, markup, afterRender);
	}

	render() {
		super.render(document.querySelector('#contentContainer'));
		history.pushState(null, '', `/${this.id}`);
	}
}

export default { Content, Page };