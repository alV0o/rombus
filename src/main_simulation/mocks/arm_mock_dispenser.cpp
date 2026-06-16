#include "rclcpp/rclcpp.hpp"
#include "rmf_dispenser_msgs/msg/dispenser_request.hpp"
#include "rmf_dispenser_msgs/msg/dispenser_result.hpp"
#include "string"

//заглушка робота-погрузчика 
class ArmMockDispenser : public rclcpp::Node
{
public:
    ArmMockDispenser() : Node("arm_mock_dispenser")
    {
        
        this->declare_parameter<std::string>("rmf_dispenser_name", "default_arm");
        
        this->get_parameter("rmf_dispenser_name", name);
        
        RCLCPP_INFO(this->get_logger(), "Погрузчик [%s] готов", name.c_str());
        
        request_subscription_ = this->create_subscription<rmf_dispenser_msgs::msg::DispenserRequest>(
        "dispenser_requests", 10, std::bind(&ArmMockDispenser::request_callback, this, std::placeholders::_1));
        result_publisher_ = this->create_publisher<rmf_dispenser_msgs::msg::DispenserResult>("dispenser_results", 10);
    }

private:
    void request_callback(const rmf_dispenser_msgs::msg::DispenserRequest::SharedPtr msg){
        if (msg->target_guid == name && used_requests.count(msg->target_guid) == 0){
            const auto first_item = msg->items[0];
            RCLCPP_INFO(this->get_logger(),
            "Погрузчик [%s] получил запрос на погрузку [%s] в количестве [%d]",
            name.c_str(),
            first_item.type_guid.c_str(),
            first_item.quantity);

            sleep(5);
            
            auto response = rmf_dispenser_msgs::msg::DispenserResult();
            response.request_guid = msg->request_guid;
            response.source_guid = msg->target_guid;
            response.status = rmf_dispenser_msgs::msg::DispenserResult::SUCCESS;
            result_publisher_->publish(response);
            RCLCPP_INFO(this->get_logger(), "Погрузчик [%s] завершил Погрузку", name.c_str());

            used_requests.insert(msg->request_guid);

            if (used_requests.size() > 100){
                used_requests.erase(used_requests.begin());
            }
        }
    }
    std::string name;
    rclcpp::Subscription<rmf_dispenser_msgs::msg::DispenserRequest>::SharedPtr request_subscription_;
    rclcpp::Publisher<rmf_dispenser_msgs::msg::DispenserResult>::SharedPtr result_publisher_;
    std::set<std::string> used_requests;
};

int main(int argc, char ** argv){
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ArmMockDispenser>());
    rclcpp::shutdown();
    return 0;
}