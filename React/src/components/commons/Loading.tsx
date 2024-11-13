type Props = {
  view: boolean
  message: string
}

function Loading({ view, message }: Props) {
  // console.log("Render Loading");
  
  return (
    <div className={"fixed m-3 z-50 left-0 max-w-30ch overflow-hidden bottom-0 bg-inherit " + (view ? "" : "hidden")}>
      {message}
    </div>
  )
}

export default Loading