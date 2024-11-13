import { useFormik } from "formik";
import { CreateTaskModel, Priority, PriorityColor, Status, StatusColor } from "../../models/TaskModel";
import { createTask } from "../../services/TaskService";
import { useNavigate } from "react-router-dom";

const CreateTaskComponent = () => {
  // console.log("Render CreateTaskComponent");
  const navigate = useNavigate();
  const formik = useFormik({
    initialValues: {
      summary: "",
      description: "",
      status: Status.OPEN,
      priority: Priority.MEDIUM,
    },
    // validationSchema: validationSchema,
    onSubmit: async (values) => {
      const body: CreateTaskModel = {
        summary: values.summary,
        description: values.description,
        status: values.status,
        priority: values.priority,
        user_id: undefined
      };
      await createTask(body)
        .then((res) => {
          if (res.status == 201) {
            navigate("/tasks")
          }
        })
        .catch((err) => {
          console.log(err);
        });
    }
  });
  const { handleSubmit, getFieldProps } = formik;

  return (
    <div className="max-w-md mx-auto mt-10 p-6 border border-traditional-forest-green rounded-lg dark:text-white-smoke">
      <h2 className="text-2xl font-bold mb-4">Create New Task</h2>
      <form onSubmit={handleSubmit}>
        <label className="block mb-2" htmlFor="summary">Summary:</label>
        <input
          className="input w-full mb-5"
          type="text"
          id="summary"
          {...getFieldProps("summary")}
          required
        />

        <label className="block mb-2" htmlFor="description">Description:</label>
        <textarea
          className="input w-full mb-5"
          id="description"
          rows={4}
          {...getFieldProps("description")}
        />

        <label className="block mb-2" htmlFor="priority">Priority:</label>
        <select
          className={"select-green p-2 mb-5 " + PriorityColor[formik.values.priority as keyof typeof PriorityColor]}
          id="priority"
          {...getFieldProps("priority")}
          required
        >
          {
            Object.keys(Priority).map((priority) => (
              <option key={priority} value={priority} className={"option-green"}>{priority}</option>
            ))
          }
        </select>

        <label className="block mb-2" htmlFor="status">Status:</label>
        <select
          className={"select-green p-2 mb-5 " + StatusColor[formik.values.status as keyof typeof StatusColor]}
          id="status"
          {...getFieldProps("status")}
          required
        >
          {
            Object.keys(Status).map((status) => (
              <option key={status} value={status} className={"option-green"}>{status}</option>
            ))
          }
        </select>
        <button type="submit" className="w-full button button-green">
          Create Task
        </button>
      </form>
    </div>
  )
}

export default CreateTaskComponent