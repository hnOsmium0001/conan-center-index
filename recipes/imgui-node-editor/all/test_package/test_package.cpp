#include <imgui.h>
#include <imgui_internal.h>
#include <imgui_node_editor.h>

namespace ed = ax::NodeEditor;

int main() {
  ImGui::CreateContext();
  ImGuiIO& io = ImGui::GetIO();

  // Build atlas
  unsigned char *tex_pixels = NULL;
  int tex_w, tex_h;
  io.Fonts->GetTexDataAsRGBA32(&tex_pixels, &tex_w, &tex_h);

  ed::Config config;
  config.SettingsFile = "test_package.json";
  auto context = ed::CreateEditor(&config);

  ImGui::NewFrame();
  ImGui::Begin("Content");

  ed::SetCurrentEditor(context);
  ed::Begin("My editor", ImVec2(0.0f, 0.0f));
  int uniqueId = 0;
  ed::BeginNode(uniqueId++);
  {
    ImGui::Text("Node A");
    ed::BeginPin(uniqueId++, ed::PinKind::Input);
      ImGui::Text("-> In");
    ed::EndPin();
    ImGui::SameLine();
    ed::BeginPin(uniqueId++, ed::PinKind::Output);
      ImGui::Text("Out ->");
    ed::EndPin();
  }
  ed::EndNode();
  ed::End();
  ed::SetCurrentEditor(nullptr);

  ImGui::End();
  ImGui::Render();

  ed::DestroyEditor(context);
  ImGui::DestroyContext();
}
