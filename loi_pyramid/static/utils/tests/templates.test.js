import templates from '../templates.js'
import { mockListener, mockTemplate, mockPage, mockEventFunction } from './__mocks__/templates.js'

// the practice of using the dom for these unit mocks is possibly problematic
const mockPageContainer = document.createElement('div')
mockPageContainer.id = 'pageContainer'
document.body.appendChild(mockPageContainer)
const newContainer = document.createElement('div')
newContainer.id = 'newContent'
document.body.appendChild(newContainer)

beforeEach(() => {
  mockPageContainer.innerHTML = ''
  newContainer.innerHTML = ''
  expect(mockPageContainer.children.length).toBe(0)
  expect(newContainer.children.length).toBe(0)
})

// This probably tests too many implementation details

test('new listener()', () => {
  expect(mockListener).toBeTruthy()

  // test that we don't have access to the internals
  expect(mockListener.elementPath).toBeFalsy()
  expect(mockListener.eventType).toBeFalsy()
  expect(mockListener.eventFunction).toBeFalsy()

  expect(mockListener.attrs().elementPath).toBe('div')
  expect(mockListener.attrs().eventType).toBe('focus')
  expect(mockListener.attrs().eventFunction).toBe(mockEventFunction)
  expect(mockListener.attrs().container).toBeFalsy()
  expect(mockListener.attrs().element).toBeFalsy()
})

// TODO: add listener render

// Could this be a candidate for an integration test?
// Or at least to replace container with a non dom object
test('assign content()', () => {
  const newContent = templates.content(mockTemplate, newContainer)
  expect(newContent).toBeTruthy()

  // test we don't have access to the internals
  expect(newContent.markup).toBeFalsy()
  expect(newContent.listeners).toBeFalsy()
  expect(newContent.dataset).toBeFalsy()
  expect(newContent.renderData).toBeFalsy()

  newContent.attrs().renderData()

  expect(newContent.attrs().markup).toBe('<div class="mock"></div>')
  expect(newContent.attrs().listeners[0]).toBe(mockListener)
  expect(newContent.attrs().dataset).toBeTruthy()
  expect(newContent.attrs().renderData).toHaveBeenCalled()
})

test('content render()', () => {
  const newContent = templates.content(mockTemplate, newContainer)
  expect(newContent).toBeTruthy()

  newContent.render()

  expect(newContent.attrs().container.children[0].className).toBe('mock')
  expect(newContent.attrs().renderData).toHaveBeenCalled()

  // purposely not testing the listeners here, those need to be integration
})

test('page()', () => {
  expect(mockPage).toBeTruthy()

  // test that we don't have access to the internals
  expect(mockPage.container).toBeFalsy()
  expect(mockPage.path).toBeFalsy()
  expect(mockPage.markup).toBeFalsy()
  expect(mockPage.templateMap).toBeFalsy()
  expect(mockPage.contentMap).toBeFalsy()

  expect(mockPage.attrs().container).toBeFalsy()
  expect(mockPage.attrs().path).toBe('mock')
  expect(mockPage.attrs().markup).toBe('<div id="sampleContent"></div>')
  expect(mockPage.attrs().templateMap.sampleContent).toBe(mockTemplate)
  expect(mockPage.attrs().contentMap).toEqual({})
})

// Using window pathname expectations here might be better for integration tests
test('page render()', () => {
  mockPage.render(mockPageContainer)

  expect(mockPage.attrs().container.id).toBe('pageContainer')
  expect(mockPage.attrs().container.children[0].id).toBe('sampleContent')
  expect(mockPage.attrs().container.children[0].children[0].className).toBe('mock')
  expect(mockPage.attrs().contentMap.sampleContent.attrs().container).toBeInstanceOf(HTMLDivElement)

  expect(window.location.pathname).toBe('/app/mock')
})

// Using window pathname expectations here might be better for integration tests
test('page render() over existing page', () => {
  mockPageContainer.appendChild(newContainer)

  mockPage.render(mockPageContainer)

  expect(mockPage.attrs().container.children[0].id).toBe('sampleContent')
  expect(mockPage.attrs().container.children[0].children[0].className).toBe('mock')
  expect(mockPage.attrs().contentMap.sampleContent.attrs().container).toBeInstanceOf(HTMLDivElement)
})

// Using window pathname expectations here might be better for integration tests
test('page clear() over existing page', () => {
  mockPageContainer.appendChild(newContainer)

  mockPage.clear()

  expect(mockPage.attrs().container).toBeFalsy()
  expect(mockPage.attrs().contentMap).toEqual({})
})
