
const mockEventFunction = jest.fn(event => {
  event.preventDefault()
})

const mockListener = (container, element) => {
  const elementPath = 'div'
  const eventType = 'focus'
  const eventFunction = mockEventFunction

  // let setContainer = newContainer => container = newContainer
  // let setElement = newElement => element = newElement

  const attrs = () => {
    return {
      elementPath: elementPath,
      eventType: eventType,
      eventFunction: eventFunction,
      container: container,
      element: element
    }
  }

  return {
    attrs: attrs//,
    // setContainer: setContainer,
    // setElement: setElement
  }
}

const listenable = {
  render: () => {
    this.element.addEventListener(this.eventType, this.eventFunction)
  },
  clear: () => {
    this.element.removeEventListener(this.eventType, this.eventFunction)
  }
}

const newContainer = document.createElement('div')
newContainer.id = 'newContent'
document.body.appendChild(newContainer)

const newForm = document.createElement('form')
newForm.id = 'newForm'
newContainer.appendChild(newForm)

test('new listener()', () => {
  const newListener = Object.create(mockListener(newContainer, newForm))

  expect(newListener).toBeTruthy()

  // test that we don't have access to the internals
  expect(newListener.elementPath).toBeFalsy()
  expect(newListener.eventType).toBeFalsy()
  expect(newListener.eventFunction).toBeFalsy()

  expect(newListener.attrs().elementPath).toBe('div')
  expect(newListener.attrs().eventType).toBe('focus')
  expect(newListener.attrs().eventFunction).toBe(mockEventFunction)
  expect(newListener.attrs().container).toBe(newContainer)
  expect(newListener.attrs().element).toBe(newForm)
})

test('create listener()', () => {
  let newListener = Object.create(mockListener(newContainer, newForm))
  newListener = Object.assign(newListener, listenable)

  expect(newListener).toBeTruthy()

  // test that we don't have access to the internals
  expect(newListener.elementPath).toBeFalsy()
  expect(newListener.eventType).toBeFalsy()
  expect(newListener.eventFunction).toBeFalsy()

  expect(newListener.attrs().elementPath).toBe('div')
  expect(newListener.attrs().eventType).toBe('focus')
  expect(newListener.attrs().eventFunction).toBe(mockEventFunction)
  expect(newListener.attrs().container).toBe(newContainer)
  expect(newListener.attrs().element).toBe(newForm)

  /*
  newListener.render()
  newForm.dispatchEvent(new Event('focus', { bubbles: true }))

  expect(mockEventFunction).toHaveBeenCalledTimes(1)

  newListener.clear()
  newForm.dispatchEvent(new Event('focus', { bubbles: true }))

  expect(mockEventFunction).toHaveBeenCalledTimes(1)
  */
})
